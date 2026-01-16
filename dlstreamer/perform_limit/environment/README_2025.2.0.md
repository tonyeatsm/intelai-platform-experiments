# Doc

```shell

# dlstreamer
https://github.com/open-edge-platform/dlstreamer

# tutorial
https://dlstreamer.github.io/get_started/tutorial.html


```

# Docker pull

```shell

sudo docker pull intel/dlstreamer:2025.2.0-ubuntu22


```

# Docker create

```shell

sudo docker run -itd \
--restart always \
--name intelai-platform-experiments_dlstreamer-2025.2.0 \
--user root \
--device /dev/dri/renderD129:/dev/dri/renderD129 \
-v /etc/localtime:/etc/localtime \
--ipc=host \
-v /data/intel-workspace/intelai-platform-experiments/dlstreamer:/root/dlstreamer \
-w /root/dlstreamer intel/dlstreamer:2025.2.0-ubuntu22


```

# Docker enter

```shell

sudo docker start intelai-platform-experiments_dlstreamer-2025.2.0
sudo docker exec -it intelai-platform-experiments_dlstreamer-2025.2.0 /bin/bash

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

# CPU and Memory affinity
```shell

numactl --hardware
available: 1 nodes (0)
node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
node 0 size: 31335 MB
node 0 free: 9708 MB
node distances:
node   0 
  0:  10 

lscpu -e=CPU,CORE,SOCKET,NODE
CPU CORE SOCKET NODE
  0    0      0    0
  1    0      0    0
  2    1      0    0
  3    1      0    0
  4    2      0    0
  5    2      0    0
  6    3      0    0
  7    3      0    0
  8    4      0    0
  9    4      0    0
 10    5      0    0
 11    5      0    0
 12    6      0    0
 13    7      0    0
 14    8      0    0
 15    9      0    0
 16   10      0    0
 17   11      0    0
 18   12      0    0
 19   13      0    0

Small cores do not have hyperthreading; cores 12-19 are small cores.
Add `--cap-add=SYS_NICE` to the container startup.

```

# Perform limit 
```shell
numactl --physcpubind=0-1 --membind=0 \
numactl --physcpubind=2-3 --membind=0 \
numactl --physcpubind=4-5 --membind=0 \
numactl --physcpubind=6-7 --membind=0 \
numactl --physcpubind=8-9 --membind=0 \
numactl --physcpubind=10-11 --membind=0 \


numactl --physcpubind=0-1 --membind=0 \
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