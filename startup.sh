
# This is for reinstalling OpenCV using CUDA
# # check your memory first
# free -m
# # you need at least a total of 8.5 GB!
# # if not, enlarge your swap space as explained in the guide
# wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-6-0.sh
# sudo chmod 755 ./OpenCV-4-6-0.sh
# ./OpenCV-4-6-0.sh
# # once the installation is done...
# rm OpenCV-4-6-0.sh
# # just a tip to save an additional 275 MB
# sudo rm -rf ~/opencv
# sudo rm -rf ~/opencv_contrib

# Install Pytorch 1.13.0
wget https://developer.download.nvidia.com/compute/redist/jp/v502/pytorch/torch-1.13.0a0+d0d6b1f2.nv22.10-cp38-cp38-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev libomp-dev -y
pip3 install 'Cython<3'
pip3 install numpy torch-1.13.0a0+d0d6b1f2.nv22.10-cp38-cp38-linux_aarch64.whl

# Install Torchvision 0.14.1
# Must create affine_quantizer.h symlink to AffineQuantizer.h
ln -s ~/.local/lib/python3.8/site-packages/torch/include/ATen/native/quantized/AffineQuantizer.h \
    ~/.local/lib/python3.8/site-packages/torch/include/ATen/native/quantized/affine_quantizer.h

sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev -y
git clone --branch v0.14.1 https://github.com/pytorch/vision torchvision 
cd torchvision
export BUILD_VERSION=0.14.1 
python3 setup.py install --user
cd ../  # attempting to load torchvision from build dir will result in import error

pip3 install onnx==1.16.0
pip3 install numpy==1.20.3
pip3 install ultralytics==8.1.37
pip3 uninstall opencv-python -y

echo "Pytorch 1.13.0"
echo "Torchvision 0.14.1"
echo "ultralytics 8.1.37 "
echo "onnx 1.16.0"
echo "numpy 1.20.3"
echo "Requirements Installation Complete. Please reboot your Jetson."
