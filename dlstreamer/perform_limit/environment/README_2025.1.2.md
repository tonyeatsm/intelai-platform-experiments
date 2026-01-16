# Doc

```shell

# dlstreamer
https://github.com/open-edge-platform/dlstreamer

# tutorial
https://dlstreamer.github.io/get_started/tutorial.html


```

# Docker pull

```shell

sudo docker pull intel/dlstreamer:2025.1.2-ubuntu22


```

# Docker create

```shell

sudo docker run -itd \
--restart always \
--name intelai-platform-experiments_dlstreamer-2025.1.2 \
--user root \
--device /dev/dri/renderD129:/dev/dri/renderD129 \
-v /etc/localtime:/etc/localtime \
--ipc=host \
-v /data/intel-workspace/intelai-platform-experiments/dlstreamer:/root/dlstreamer \
-w /root/dlstreamer intel/dlstreamer:2025.1.2-ubuntu22


```

# Docker enter

```shell

sudo docker start intelai-platform-experiments_dlstreamer-2025.1.2
sudo docker exec -it intelai-platform-experiments_dlstreamer-2025.1.2 /bin/bash

apt update
apt install -y wget unzip

pip install ultralytics==8.3.222 -i https://mirrors.aliyun.com/pypi/simple

```

# Models
```shell

# Download model
mkdir -p /root/dlstreamer/perform_limit/models
cd /root/dlstreamer/perform_limit/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
# Convert model to OpenVINO IR
python3 /root/dlstreamer/perform_limit/src/convert_model.py


```

# Data
```shell

mkdir -p /root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps
cd /root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps
wget https://videos.pexels.com/video-files/1192116/1192116-sd_640_360_30fps.mp4

rm -rf /root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input
rm -rf /root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/segments

cd /root/dlstreamer/perform_limit/scripts
chmod +x gen_random_videos.sh
./gen_random_videos.sh

```

# Perform limit 
```shell


gst-launch-1.0 \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1 \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  \
filesrc location=/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_8.mp4 ! \
qtdemux ! h264parse ! vah264dec ! \
videorate ! video/x-raw,framerate=25/1 ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/perform_limit/models/yolo11n_openvino_model_static/batch8/yolo11n.xml \
    device=GPU \
    batch-size=8 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter interval=1  ! \
fakesink 








```