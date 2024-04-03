# YOLOv8-for-Jetson-Orin
- Demo code for YOLOv8 with single CSI Camera of Jetson Orin nano  
- For user convenience, just running "start.sh" -> "demo.sh" will show YOLOv8 demonstaration on your jetson board  
- Modified from https://github.com/JetsonHacksNano/CSI-Camera.git  

## Before you go
This code is for Jetpack 5.1.3, so ENSURE that your jetson is using Jetpack 5.1.3  

- Jetpack 6.0 will work too but compatible with another version of Pytorch(2.1.0) & Torchvision(0.16.1)  
- So if you are in Jetpack 6.0, edit these versions in "startup.sh"  

Version differences of main packages are described in appendix for someone in need

## Virtual Environment User
If you are going to use this code in virtual environment, please check your OpenCV build informantion in your virtual environment(NOT HOST)
```shell
$ python3
$ >>> import cv2
$ >>> print(cv2.getBuildInformation())
```
From this information, you can run this code if only "GStreamer" is "YES"
- If this is "NO", then you should use your host environment

Please check your host environment OpenCV too for sure

- SDK will automatically installed OpenCV with GStreamer "YES"  
- But if it says "NO" in host environment, you may install "opencv-python" additionally so uninstall it  
```shell
pip3 uninstall opencv-python
```

## Start Up (DO NOT USE sudo FOR startup.sh)
Preparing environmet for running YOLOv8 in Jetson, using CSI Camera  
> OpenCV 4.5.4 (SDK already installed it for you)  
> GStreamer 1.16.3 (SDK already installed it for you)  
> Pytorch 1.13.0  
> Torchvision 0.14.1  
> ultralytics 8.1.37  
> onnx 1.16.0  
> numpy 1.20.3  

Installation of Pytorch and Torchvision are from https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048  

**DO NOT USE 'sudo' command**
- Since we build torchvision from source, if you execute startup.sh with sudo, torchvision will be accessible only with sudo command  
```shell  
sh startup.sh 
```

## Demo Setup Description
This code is using YOLOv8 model for demonstration  

**Model Setting**
- 80 classes to predict
- Basically YOLOv8n is included in each directory (Model in FP16 and FP32 will be converted when you run it)    
- If you want another version like "YOLOv8m", "YOLOv8l" etc.. just replace it in every directory  

**Image Setting**
> Capture Width = 1920  
> Capture Height = 1080  
> Display Width = 640  
> Display Height = 360  

**Error Handling**  
For generality there are some "rm" and "export" command to cope with some errors may occur
- Cannot allocate memory in static TLS block  
> For these error, we have to preload modules "libgstnvarguscamerasrc.so" and "libgstnvvidconv.so"  
- Stalled when building GStreamer pipeline  
> There are some cases that GStreamer register "libgstnvarguscamerasrc.so" to its BLACKLIST.  
> With this situation, demo.sh will just stunned with no error message which makes you suffer.  
> To solve this problem, we should remove GStreamer cache.  

## Demonstration
After running "startup.sh" please reboot your jetson for safety.  

For demonstration, you should select model and framerate.  

There are 3 models (PLEASE pass exact parser)  
- **Original**: Original YOLOv8 model from ultralytics package  
- **TensorRT-FP16**: TensorRT converted model with FP16  
- **TensorRT-FP32**: TensorRT converted model with FP32  
- **Framerate**: Recommanded about 15~25  
```shell  
sh demo.sh {MODEL_NAME} {FRAMERATE}  
```

## Appendix

**Jetpack 5.1.3**
> Ubuntu: 20.04  
> Linux kernel: 5.10 LTS  
> OS: L4T 35.5.0  
> CUDA: 11.4.19  
> cuDNN: 8.6.0  
> TensorRT 8.5.2  
> VPI: 2.4  
> OpenCV: 4.5.4  
> GStreamer: 1.16.3  
> Python2: 2.7.18  
> Python3: 3.8.10  

**Jetpack 6.0**
> Ubuntu: 22.04  
> Linux kernel: 5.15 LTS  
> OS: L4T 36.2  
> CUDA: 12.2.12  
> cuDNN: 8.9.4  
> TensorRT 8.6.2  
> VPI: 3.0  
> OpenCV: 4.8.0  
> GStreamer: 1.16.3  
> Python2: 2.7.18  
> Python3: 3.10.12  
