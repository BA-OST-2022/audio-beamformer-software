import cv2
import numpy as np
import os

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

class FaceTracking():

    def __init__(self, lifetime):
        self.fd = FaceDetector()

        self.Ts = 1/30
        self.R = 507
        self.Qp = 10
        self.Qv = 0.01

        self.faces = []
        self.lifetime = lifetime

        self.focus = 0
    
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


            dist = np.linalg.norm(z_k - x_k)
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
        
        if self.focus + 1 > len(self.faces):
            self.focus = 0

        for i, fac in enumerate(self.faces):
            if np.max(np.linalg.eig(fac.P[:2, :2])[0]) < 1000:
                if i == self.focus and fac.lifetime >= self.lifetime / 2:
                    cv2.circle(img, tuple([int(x) for x in fac.get_position()]), radius=0, color=(255, 0, 0), thickness=20)
                elif fac.lifetime >= self.lifetime / 2:
                    cv2.circle(img, tuple([int(x) for x in fac.get_position()]), radius=0, color=(0, 0, 255), thickness=20)
        for box in boxes:
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        
        return img
    
    def getDetectionCount(self):
        return len(self.faces)
    
    def setFocus(self, focus):
        if focus + 1 > len(self.faces):
            self.focus = 0
        else:
            self.focus = focus
    
    def getFocus(self):
        return self.focus
    
    def getFocusLocation(self):
        if len(self.faces) > 0:
            return self.faces[self.focus].get_position()
    

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "dance3.mp4"

    cap = cv2.VideoCapture(os.path.join(dir_path, filename))

    tracker = FaceTracking(lifetime=50)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img = tracker.runDetection(frame)

        print(tracker.getDetectionCount())
        print(tracker.getFocusLocation())


        cv2.imshow("frame", img)
        key = cv2.waitKey(1)

        if key == ord('s'):
            tracker.setFocus(tracker.getFocus() + 1)
    
    cap.release()
    cv2.destroyAllWindows()