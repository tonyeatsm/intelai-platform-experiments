
# Doc
```shell

# 在家造AI神器！OpenVINO™让桌面推理触手可及
https://inteldevzone.blog.csdn.net/article/details/148951180


```

# Run
```shell

sudo docker exec -it intelai-platform-experiments_openvino /bin/bash

source /opt/benchmark-app_venv/bin/activate  

# Download model
mkdir -p /root/openvino/sources/benchmark_app/models
cd /root/openvino/sources/benchmark_app/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt

# Convert model to OpenVINO IR
python /root/openvino/sources/benchmark_app/convert_model.py

# find device
python /root/openvino/sources/device/verify_device.py

['CPU', 'GPU.0', 'GPU.1']
['13th Gen Intel(R) Core(TM) i9-13900HK', 'Intel(R) Iris(R) Xe Graphics (iGPU)', 'Intel(R) Arc(TM) A770 Graphics (dGPU)']

# 吞吐模式下帧率（单位：FPS）
benchmark_app \
-m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
-shape "x[1,3,640,640]" \
-hint throughput \
-t 600 \
-d CPU #GPU.0 GPU.1

[ INFO ] Execution Devices:['CPU']
[ INFO ] Count:            5388 iterations
[ INFO ] Duration:         60068.35 ms
[ INFO ] Latency:
[ INFO ]    Median:        57.83 ms
[ INFO ]    Average:       66.74 ms
[ INFO ]    Min:           29.11 ms
[ INFO ]    Max:           148.62 ms
[ INFO ] Throughput:   89.70 FPS

[ INFO ] Execution Devices:['GPU.0']
[ INFO ] Count:            10432 iterations
[ INFO ] Duration:         60037.28 ms
[ INFO ] Latency:
[ INFO ]    Median:        22.85 ms
[ INFO ]    Average:       22.86 ms
[ INFO ]    Min:           11.23 ms
[ INFO ]    Max:           29.91 ms
[ INFO ] Throughput:   173.76 FPS

[ INFO ] Execution Devices:['GPU.1']
[ INFO ] Count:            67840 iterations
[ INFO ] Duration:         61070.79 ms
[ INFO ] Latency:
[ INFO ]    Median:        112.96 ms
[ INFO ]    Average:       113.16 ms
[ INFO ]    Min:           35.71 ms
[ INFO ]    Max:           1060.00 ms
[ INFO ] Throughput:   1110.84 FPS


# 时延模式下帧率（单位：FPS）
benchmark_app \
-m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
-shape "x[1,3,640,640]" \
-hint latency \
-t 600 \
-d CPU #GPU.0 GPU.1

[ INFO ] Execution Devices:['CPU']
[ INFO ] Count:            24626 iterations
[ INFO ] Duration:         60001.43 ms
[ INFO ] Latency:
[ INFO ]    Median:        2.37 ms
[ INFO ]    Average:       2.39 ms
[ INFO ]    Min:           2.32 ms
[ INFO ]    Max:           5.10 ms
[ INFO ] Throughput:   410.42 FPS

[ INFO ] Execution Devices:['GPU.0']
[ INFO ] Count:            28722 iterations
[ INFO ] Duration:         60000.28 ms
[ INFO ] Latency:
[ INFO ]    Median:        2.02 ms
[ INFO ]    Average:       2.05 ms
[ INFO ]    Min:           1.86 ms
[ INFO ]    Max:           3.75 ms
[ INFO ] Throughput:   478.70 FPS

[ INFO ] Execution Devices:['GPU.1']
[ INFO ] Count:            24762 iterations
[ INFO ] Duration:         60000.92 ms
[ INFO ] Latency:
[ INFO ]    Median:        2.29 ms
[ INFO ]    Average:       2.37 ms
[ INFO ]    Min:           1.93 ms
[ INFO ]    Max:           6.39 ms
[ INFO ] Throughput:   412.69 FPS

```