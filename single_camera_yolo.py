# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import argparse
import torch
import torchvision
from ultralytics import YOLO
import numpy as np
import os

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""
def parser_for_model():
    parser = argparse.ArgumentParser(description="Model Selection")
    parser.add_argument(
        "-m", "--mode",
        type=str,
        required=True,
        default='TensorRT-FP16',
        help='Select what model to use, Original, TensorRT-FP16, TensorRT-FP32'
    )
    parser.add_argument(
        "-fr", "--framerate",
        type=int,
        default=15,
        required=True,
        help="Enter framerate. High framerate can cause output delay",

    )
    return parser

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=640,
    display_height=360,
    framerate=15,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera(args, model, Object_classes, Object_colors):
    window_title = "CSI Camera"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(framerate=args.framerate, flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    pred=model(frame, stream=True)
                    for r in pred:
                        obj=r.boxes
                        for box in obj:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            #x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            score = round(float(box.conf[0]), 2)
                            label = int(box.cls[0])
                            color = Object_colors[label]
                            cls_name = Object_classes[label]
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            cv2.putText(frame, f"{cls_name} {score}", (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 1, cv2.LINE_AA)

                    cv2.imshow(window_title, frame)
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    Object_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                'hair drier', 'toothbrush' ]
    
    Object_colors = list(np.random.rand(80,3)*255)

    args = parser_for_model().parse_args()
    
    if args.mode == 'Original':
        model = YOLO("Original/yolov8n.pt",  task='detect')
    
    elif args.mode == 'TensorRT-FP16':
        file_path=("FP16")
        file_list=os.listdir(file_path)
        if not any(file.endswith('.engine') for file in file_list):
            tgtmodel = YOLO("FP16/yolov8n.pt")
            print("Building TensorRT-FP16 Model of YOLOv8\n")
            tgtmodel.export(format='engine', device=0, half=True)
            print("Building Complete\n")
        model=YOLO("FP16/yolov8n.engine", task='detect')

    elif args.mode == 'TensorRT-FP32':
        file_path=("FP32")
        file_list=os.listdir(file_path)
        if not any(file.endswith('.engine') for file in file_list):
            tgtmodel = YOLO("FP32/yolov8n.pt")
            print("Building TensorRT-FP32 Model of YOLOv8\n")
            tgtmodel.export(format='engine', device=0, half=False)
            print("Building Complete\n")
        model=YOLO("FP32/yolov8n.engine", task='detect')

    else:
        print("Model Selection Error")
        raise AssertionError("Model Error: Please select model from 'Original', 'TensorRT-FP16', 'TensorRT-FP32'")
    
    print(f"Using {args.mode} Model")
    
    # Run Model
    show_camera(args, model, Object_classes, Object_colors)
