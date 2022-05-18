###############################################################################
# file    FaceTracking.py
###############################################################################
# brief   This module analyses image data and runs a face detection algorithm
###############################################################################
# author  Luca Jost & Florian Baumgartner & Thierry Schwaller
# version 1.0
# date    2022-05-08
###############################################################################
# MIT License
#
# Copyright (c) 2022 ICAI Interdisciplinary Center for Artificial Intelligence
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

import sys
import cv2
import numpy as np
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(__file__) + "/FaceTracking")

from FaceDetector import FaceDetector
from KalmanFilter2D import KalmanFilter2D

def closest_pairs(array1, array2):
    array1 = np.asarray(array1)
    array2 = np.asarray(array2)
    diff = np.abs(array1[:, None] - array2[None, :])
    pairs = []
    found = []
    for _ in range(np.min(diff.shape)):
        idx = np.argmin(diff)
        x,y = np.unravel_index(idx, diff.shape)
        diff[x,:] = 10000
        diff[:,y] = 10000
        pairs.append((x,y))
        found.append(x)
    unassigned = np.setdiff1d(np.arange(len(array1)), found)
    return pairs, unassigned


def rounded_rectangle(src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])

    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:

        #big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
        [top_left_main_rect, bottom_right_main_rect], 
        [top_left_rect_left, bottom_right_rect_left], 
        [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

    return src


def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background



class FaceTracking():
    def __init__(self, lifetime):
        self.fd = FaceDetector()

        self.Ts = 1/15
        self.R = 507
        self.Qp = 10
        self.Qv = 0.01

        self.faces = []
        self.lifetime = lifetime
        
        self.colorActive = (0xEA, 0xDE, 0x80)
        self.colorInactive = (0x60, 0x60, 0x60)

        self._focus = 0
        self._showDot = False
        self._showRoundRect = True
        self._enableMagic = False
    
    def __del__(self):
        self.fd.__del__()
        

    def runDetection(self, img):
        boxes, centers, labels, probs = self.fd.process(img)

        center_list = [p[0] for p in centers]
        face_list = [p.get_position()[0] for p in self.faces]

        if len(self.faces) < len(boxes):
            self.faces.append(KalmanFilter2D(self.Ts, self.R, self.Qp, self.Qv))

        pairs, unassigned = closest_pairs(face_list, center_list)

        for face_index, center_index in pairs:
            
            if self.faces[face_index].lifetime < self.lifetime:
                self.faces[face_index].inc()

            z_k = np.asarray(centers[center_index])
            x_k = self.faces[face_index].get_position()
            
            self.faces[face_index].rawBox = boxes[center_index]


            # dist = np.linalg.norm(z_k - x_k)
            mah_dist = np.sqrt(((z_k - x_k)[None] @ np.linalg.inv(self.faces[face_index].P[:2, :2]) @ (z_k - x_k)[:, None])[0,0])

            R = mah_dist*10

            self.faces[face_index].run_filter(z_k, R)

        pop_index = -1
        for face_index in unassigned:
            self.faces[face_index].dec()
            self.faces[face_index].run_filter(np.zeros((2,)), 10000000)
        
            if(self.faces[face_index].lifetime < 0):
                pop_index = face_index

        if pop_index != -1:    
            self.faces.pop(face_index)
        
        if self._focus + 1 > len(self.faces):
            self._focus = 0

        for i, fac in enumerate(self.faces): 
            if (np.max(np.linalg.eig(fac.P[:2, :2])[0]) < 1000) and (fac.lifetime >= self.lifetime / 2):
                box = fac.rawBox
                color = self.colorInactive
                if i == self._focus:
                    color = self.colorActive
                if not self._enableMagic:
                    if self._showDot:
                        cv2.circle(img, tuple([int(x) for x in fac.get_position()]), radius=0, color=color, thickness=20)
                    if self._showRoundRect:
                        rounded_rectangle(img, (box[0], box[1]), (box[3], box[2]), radius=0.3, color=color, thickness=4)
                    else:
                        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color=color, thickness=4)
                else:
                    overlay = cv2.imread('magic.png', cv2.IMREAD_UNCHANGED)
                    targetWidth = abs(box[2] - box[0])
                    targetHeight = abs(box[3] - box[1])
                    imageWidth = np.shape(overlay)[0]
                    imageHeight = np.shape(overlay)[1]
                    ratioWidth = targetWidth / imageWidth
                    ratioHeight = targetHeight / imageHeight
                    
                    width = int(imageWidth * ratioWidth)
                    height = int(imageHeight * ratioWidth)
                    if(height < targetHeight):
                        width = int(imageWidth * ratioHeight)
                        height = int(imageHeight * ratioHeight)
                        
                    x = int(fac.get_position()[0] - width // 2)
                    y = int(fac.get_position()[1] - height // 2)
                    overlay = cv2.resize(overlay, (width, height), interpolation = cv2.INTER_AREA)
                    img = overlay_transparent(img, overlay, x, y)

       
        return img
    
    
    def getDetectionCount(self):
        return len(self.faces)
    
    def setFocus(self, focus):
        if focus + 1 > len(self.faces):
            self._focus = 0
        else:
            self._focus = focus
    
    def getFocus(self):
        return self._focus
    
    def getFocusLocation(self):
        if len(self.faces) > 0:
            return self.faces[self._focus].get_position()
        else:
            return []
        
    def enableMagic (self, state):
        self._enableMagic = state
    

faceTracking = FaceTracking(lifetime=15)

if __name__ == "__main__": 
    VIDEO_FILE = "dance2.mp4"
    USE_CAMERA = True
    
    # faceTracking.enableMagic(True)
    
    if USE_CAMERA:
        cap = cv2.VideoCapture(0)
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cap = cv2.VideoCapture(os.path.join(dir_path, "demos", VIDEO_FILE))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img = faceTracking.runDetection(frame)
        print(faceTracking.getDetectionCount(), faceTracking.getFocusLocation())

        cv2.imshow("FaceTracking [ESC to quit]", img)
        key = cv2.waitKey(1)
        if key == ord('s'):
            faceTracking.setFocus(faceTracking.getFocus() + 1)
        if cv2.waitKey(1) == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()