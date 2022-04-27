import cv2
import numpy as np
import os

from FaceDetector import FaceDetector
from KalmanFilter2D import KalmanFilter2D


dir_path = os.path.dirname(os.path.realpath(__file__))
filename = "dance2.mp4"

cap = cv2.VideoCapture(0)#f"{dir_path}/{filename}")

fd = FaceDetector()

Ts = 1/30
R = 50
Qp = 10
Qv = 0.01

faces = [KalmanFilter2D(Ts, R, Qp, Qv) for _ in range(3)]

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

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:

        boxes, centers, labels, probs = fd.process(frame)

        center_list = [p[0] for p in centers]
        face_list = [p.get_position()[0] for p in faces]

        pairs, unassigned = closest_pairs(face_list, center_list)

        for face_index, center_index in pairs:
            z_k = np.asarray(centers[center_index])
            x_k = faces[face_index].get_position()

            dist = np.linalg.norm(z_k - x_k)
            mah_dist = np.sqrt(((z_k - x_k)[None] @ np.linalg.inv(faces[face_index].P[:2, :2]) @ (z_k - x_k)[:, None])[0,0])

            R = mah_dist*10
            # R = dist+10

            faces[face_index].run_filter(z_k, R)

        for face_index in unassigned:
            faces[face_index].run_filter(np.zeros((2,)), 10000000)

        for i, fac in enumerate(faces):
            if np.max(np.linalg.eig(fac.P[:2, :2])[0]) < 1000:
                cv2.circle(frame, tuple([int(x) for x in fac.get_position()]), radius=0, color=(255 - 255*i, 0, i*255), thickness=20)
        for box in boxes:
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        cv2.imshow('Face Detector', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

cap.release()
cv2.destroyAllWindows()