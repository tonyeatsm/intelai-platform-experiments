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
mkdir -p /root/dlstreamer/stream_batch_error/models
cd /root/dlstreamer/stream_batch_error/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
# Convert model to OpenVINO IR
python3 /root/dlstreamer/stream_batch_error/src/convert_model.py


```

# Data
```shell

mkdir -p /root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps
cd /root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps
wget https://videos.pexels.com/video-files/1192116/1192116-sd_640_360_30fps.mp4

rm -rf /root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/input
rm -rf /root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/segments

cd /root/dlstreamer/stream_batch_error/scripts
chmod +x gen_random_videos.sh
./gen_random_videos.sh

```

# Dynamic batch start error
```shell

# gst-launch
gst-launch-1.0 filesrc location=/root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_1.mp4 ! \
qtdemux ! \
h264parse ! \
vah264dec ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/stream_batch_error/models/yolo11n_openvino_model_dynamic/yolo11n.xml \
    device=GPU \
    batch-size=1 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter ! \
fakesink

# error log
root@58f49b639a56:~/dlstreamer# gst-launch-1.0 filesrc location=/root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_1.mp4 ! \
qtdemux ! \
h264parse ! \
vah264dec ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/stream_batch_error/models/yolo11n_openvino_model_dynamic/yolo11n.xml \
    device=GPU batch-size=1 ! \
fakesink
Setting pipeline to PAUSED ...
Pipeline is PREROLLING ...
Got context from element 'vapostproc0': gst.va.display.handle=context, gst-display=(GstObject)"\(GstVaDisplayDrm\)\ vadisplaydrm3", description=(string)"Intel\(R\)\ Gen\ Graphics", path=(string)/dev/dri/renderD129;
Redistribute latency...
Redistribute latency...
ERROR: from element /GstPipeline:pipeline0/GstGvaDetect:gvadetect0: base_inference plugin initialization failed
Additional debug info:
/home/dlstreamer/dlstreamer/src/monolithic/gst/inference_elements/base/inference_singleton.cpp(181): acquire_inference_instance (): /GstPipeline:pipeline0/GstGvaDetect:gvadetect0:

display.drvVtable().vaCreateSurfaces2(display.drvCtx(), rt_format, width, height, &va_surface_id, 1, &surface_attrib, 1) failed, sts=18 invalid parameter
ERROR: pipeline doesn't want to preroll.
ERROR: from element /GstPipeline:pipeline0/GstGvaDetect:gvadetect0: base_inference based element initialization has been failed.
Additional debug info:
/home/dlstreamer/dlstreamer/src/monolithic/gst/inference_elements/base/gva_base_inference.cpp(857): gva_base_inference_set_caps (): /GstPipeline:pipeline0/GstGvaDetect:gvadetect0:

inference is NULL.
ERROR: pipeline doesn't want to preroll.
Setting pipeline to NULL ...
ERROR: from element /GstPipeline:pipeline0/GstGvaDetect:gvadetect0: base_inference plugin initialization failed
Additional debug info:
/home/dlstreamer/dlstreamer/src/monolithic/gst/inference_elements/base/inference_singleton.cpp(181): acquire_inference_instance (): /GstPipeline:pipeline0/GstGvaDetect:gvadetect0:

display.drvVtable().vaCreateSurfaces2(display.drvCtx(), rt_format, width, height, &va_surface_id, 1, &surface_attrib, 1) failed, sts=18 invalid parameter
ERROR: pipeline doesn't want to preroll.
ERROR: from element /GstPipeline:pipeline0/GstGvaDetect:gvadetect0: base_inference based element initialization has been failed.
Additional debug info:
/home/dlstreamer/dlstreamer/src/monolithic/gst/inference_elements/base/gva_base_inference.cpp(857): gva_base_inference_set_caps (): /GstPipeline:pipeline0/GstGvaDetect:gvadetect0:

inference is NULL.
ERROR: pipeline doesn't want to preroll.
ERROR: from element /GstPipeline:pipeline0/GstGvaDetect:gvadetect0: base_inference failed on stop
Additional debug info:
/home/dlstreamer/dlstreamer/src/monolithic/gst/inference_elements/base/gva_base_inference.cpp(958): gva_base_inference_stop (): /GstPipeline:pipeline0/GstGvaDetect:gvadetect0:
empty inference instance
ERROR: pipeline doesn't want to preroll.
Freeing pipeline ...


# ChatGPT error analysis
dynamic batch + GPU + VAAPI 的已知坑
DLStreamer 的 gvadetect 在 GPU + dynamic shape + VA surface 场景下经常触发
vaCreateSurfaces2 invalid parameter
关闭dynamic
model.export(format='openvino', dynamic=False)


```


# Static batch alignment error
```shell

gst-launch-1.0 filesrc location=/root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_1.mp4 ! \
qtdemux ! \
h264parse ! \
vah264dec ! \
vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/stream_batch_error/models/yolo11n_openvino_model_static/batch1/yolo11n.xml \
    device=GPU \
    batch-size=1 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter ! \
fakesink


gst-launch-1.0 \
concat name=c ! \
h264parse ! vah264dec ! vapostproc ! 'video/x-raw(memory:VAMemory),width=640,height=360' ! \
gvadetect model=/root/dlstreamer/stream_batch_error/models/yolo11n_openvino_model_static/batch2/yolo11n.xml \
    device=GPU \
    batch-size=2 \
    nireq=4 \
    pre-process-backend=vaapi-surface-sharing \
    model-instance-id=inf0 ! \
gvafpscounter ! \
fakesink \
filesrc location=/root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_1.mp4 ! qtdemux ! queue ! c. \
filesrc location=/root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/input/1192116-sd_640_360_30fps_2.mp4 ! qtdemux ! queue ! c.


no nireq 
nireq=1 260.17 fps
nireq=2 419.60 fps
nireq=3 453.20 fps

```