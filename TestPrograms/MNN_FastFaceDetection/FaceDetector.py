import os
import time
from math import ceil

import MNN
import cv2
import numpy as np
import torch

import utils.box_utils_numpy as box_utils

def predict(width, height, confidences, boxes, prob_threshold, iou_threshold=0.3, top_k=-1):
    boxes = boxes[0]
    confidences = confidences[0]
    picked_box_probs = []
    picked_labels = []
    for class_index in range(1, confidences.shape[1]):
        probs = confidences[:, class_index]
        mask = probs > prob_threshold
        probs = probs[mask]
        if probs.shape[0] == 0:
            continue
        subset_boxes = boxes[mask, :]
        box_probs = np.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
        box_probs = box_utils.hard_nms(box_probs,
                                    iou_threshold=iou_threshold,
                                    top_k=top_k,
                                    )
        picked_box_probs.append(box_probs)
        picked_labels.extend([class_index] * box_probs.shape[0])
    if not picked_box_probs:
        return np.array([]), np.array([]), np.array([])
    picked_box_probs = np.concatenate(picked_box_probs)
    picked_box_probs[:, 0] *= width
    picked_box_probs[:, 1] *= height
    picked_box_probs[:, 2] *= width
    picked_box_probs[:, 3] *= height
    return picked_box_probs[:, :4].astype(np.int32), np.array(picked_labels), picked_box_probs[:, 4]



class FaceDetector:

    image_mean = np.array([127, 127, 127])
    image_std = 128.0
    iou_threshold = 0.3
    center_variance = 0.1
    size_variance = 0.2
    min_boxes = [[10, 16, 24], [32, 48], [64, 96], [128, 192, 256]]
    strides = [8, 16, 32, 64]

    def __init__(self, interpreter = "slim-320.mnn"):
        self.input_size = [320, 240]
        shrinkage_list = []
        feature_map_w_h_list = []

        for size in self.input_size:
            feature_map = [ceil(size / stride) for stride in self.strides]
            feature_map_w_h_list.append(feature_map)

        for i in range(0, len(self.input_size)):
            shrinkage_list.append(self.strides)

        self.priors = []
        for index in range(0, len(feature_map_w_h_list[0])):
            scale_w = self.input_size[0] / shrinkage_list[0][index]
            scale_h = self.input_size[1] / shrinkage_list[1][index]
            for j in range(0, feature_map_w_h_list[1][index]):
                for i in range(0, feature_map_w_h_list[0][index]):
                    x_center = (i + 0.5) / scale_w
                    y_center = (j + 0.5) / scale_h

                    for min_box in self.min_boxes[index]:
                        w = min_box / self.input_size[0]
                        h = min_box / self.input_size[1]
                        self.priors.append([
                            x_center,
                            y_center,
                            w,
                            h
                        ])
        self.priors = torch.tensor(self.priors)

        torch.clamp(self.priors, 0.0, 1.0, out=self.priors)

        
        self.interpreter = MNN.Interpreter("models/" + interpreter)
        self.session = self.interpreter.createSession()
        self.input_tensor = self.interpreter.getSessionInput(self.session)
    
    def process(self, image):
        image_ori = image
        image = cv2.cvtColor(image_ori, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, tuple(self.input_size))
        #image = image.astype(float)
        image = (image - self.image_mean) / self.image_std
        image = image.transpose((2, 0, 1))
        image = np.asarray(image, dtype=np.float32)

        tmp_input = MNN.Tensor((1, 3, self.input_size[1], self.input_size[0]), MNN.Halide_Type_Float, image, MNN.Tensor_DimensionType_Caffe)
        self.input_tensor.copyFrom(tmp_input)
        time_time = time.time()
        self.interpreter.runSession(self.session)
        scores = self.interpreter.getSessionOutput(self.session, "scores").getData()
        boxes = self.interpreter.getSessionOutput(self.session, "boxes").getData()
        boxes = np.expand_dims(np.reshape(boxes, (-1, 4)), axis=0)
        scores = np.expand_dims(np.reshape(scores, (-1, 2)), axis=0)
        print("inference time: {} s".format(round(time.time() - time_time, 4)))
        boxes = box_utils.convert_locations_to_boxes(boxes, self.priors, self.center_variance, self.size_variance)
        boxes = box_utils.center_form_to_corner_form(boxes)
        boxes, labels, probs = predict(image_ori.shape[1], image_ori.shape[0], scores, boxes, 0.6)
        centers = []
        for i in range(boxes.shape[0]):
            box = boxes[i, :]
            centers.append([((box[2] - box[0]) / 2) + box[0], ((box[3] - box[1]) / 2) + box[1]])
        return boxes, centers, labels, probs


if __name__ == "__main__":

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "dance.mp4"

    cap = cv2.VideoCapture(f"{dir_path}\{filename}")

    fd = FaceDetector()

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            
            boxes, centers, labels, probs = fd.process(frame)

            for i in range(boxes.shape[0]):
                box = boxes[i, :]
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.circle(frame, (centers[0].astype(np.int32),centers[1].astype(np.int32)), radius=0, color=(255, 0, 0), thickness=20)
            
            cv2.imshow('Face Detector', frame)

            c = cv2.waitKey(1)
            if c == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
