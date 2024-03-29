# YOLOv8-for-Jetson-Orin
Demo code for YOLOv8 with single CSI Camera of Jetson Orin nano

## Before you go

### Jetpack Version(5.1.3)
This code is for Jetpack 5.1.3, so ENSURE that your jetson is using Jetpack 5.1.3 

> Jetpack 6.0 will work too but compatible with another version of Pytorch(2.1.0) & Torchvision(0.16.1), so if you are in Jetpack 6.0, edit these versions in "startup.sh"

Main packages version difference described below for someone in need

**Jetpack 5.1.3**
> CUDA 11.4
> OpenCV 4.5.4
> GStreamer 1.16.3
> Python2 2.7.18
> Python3 3.8.10

**Jetpack 6.0**
> CUDA 12.2
> OpenCV
> GStreamer
> Python2
> Python3

### Virtual Environment User
If you are going to use this code in virtual environment, please check your OpneCV build informantion in your virtual environment(NOT HOST)
```shell
$ python3
$ >>> import cv2
$ >>> print(cv2.getBuildInformation())
```
From this information, you can run this code if only "GStreamer" is "YES"
> If this is "NO", then you should use your host environment
Please check your host environment OpenCV too for sure
> SDK will automatically installed OpenCV with GStreamer "YES"
> But if it says "NO" in host environment, you may install opencv-python additionally so uninstall it
>> ```shell
>> pip3 uninstall opencv-python
>> ```

## Start Up (DO NOT USE sudo FOR startup.sh)

Jetpack 5.1.3
CUDA 11.4
OpenCV

For preparing environmet for running YOLOv8 in Jetson
> OpenCV 4.5.4 (SDK already installed it for you)
> GStreamer 1.16.3 (SDK already installed it for you)
> Pytorch 1.13.0  
> Torchvision 0.14.1  
> ultralytics 8.1.37
> onnx 1.16.0
> numpy 1.20.3

Installation of Pytorch and Torchvision are from https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
**DO NOT USE 'sudo' command**
> Since we build torchvision from source, if you execute startup.sh with sudo, torchvision will be accessible only with sudo command

```shell  
sh startup.sh 
```

## Demo Setup Description
This code is using YOLOv8 model for demonstration
Image Setting
> capture_width=1920
> capture_height=1080
> display_width=640
> display_height=360
There are some "rm" and "export" command in "demo.sh" to cope with some errors may occur. You can find details in code.

## Demonstration
After running "startup.sh" please reboot your jetson for safety

For demonstration, you should select model and framerate

> There are 3 models (PLEASE pass exact parser)
> - **Original** : Original YOLOv8 model from ultralytics package 
> - **TensorRT-FP16** : TensorRT converted model with FP16
> - **TensorRT-FP32** : TensorRT converted model with FP32

> Framerate is recommanded about 15~25

```shell  
sh demo.sh {MODEL_NAME} {FRAMERATE}  
```