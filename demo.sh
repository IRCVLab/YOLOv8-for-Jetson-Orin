# There are some cases that GStreamer register "libgstnvarguscamerasrc.so" to its BLACKLIST
# With this situation, demo.sh will just stunned with no error message which makes you suffer
# To solve this problem, we should remove GStreamer cache
rm ~/.cache/gstreamer-1.0/registry.aarch64.bin

#This lines are for GStreamer Error "Cannot allocate memory in static TLS block"
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvarguscamerasrc.so
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvvidconv.so

echo "model: $1"
echo "framerate: $2"
python3 single_camera_yolo.py -m "$1" -fr "$2" 