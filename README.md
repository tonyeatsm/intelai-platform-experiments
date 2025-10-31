# Intel AI Platform Experiments

Experiments and practical workflows using Intel's AI software stack to deploy and optimize AI workloads (CV, LLMs, real-time analytics) on Intel CPUs and GPUs.

## Features
- OpenVINO inference benchmarking with YOLO11n (throughput/latency)
- Device discovery for Intel AI hardware
- Dockerized environment and reusable Python venv cloning
- Optional YOLO training on Intel GPUs (PyTorch XPU)

## Tech Stack
- [OpenVINO](https://docs.openvino.ai/)
- [PyTorch XPU (Intel GPU)](https://download.pytorch.org/whl/nightly/xpu)
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [oneAPI/SYCL](https://www.oneapi.com/)

## Repository Layout
```text
openvino/
  environment/           # Docker usage and venv cloning
    clone-venv.sh
    README.md
  sources/
    benchmark_app/       # OpenVINO model convert + benchmark flow
      convert_model.py
      models/
      README.md
    device/              # Device discovery
      verify_device.py
      README.md
    xpu_training/        # YOLO training on Intel GPU (optional)
      yolo/
        README.md
README.md                # English README
README.zh-CN.md          # Chinese README
```

## Quickstart
1) Clone
```bash
git clone https://github.com/tonyeatsm/intelai-platform-experiments.git
cd intelai-platform-experiments
```

2) Start Docker environment (recommended). See `openvino/environment/README.md` for details.
```bash
sudo docker pull openvino/ubuntu24_dev:2025.3.0
sudo docker run -itd \
  --restart always \
  --name intelai-platform-experiments_openvino \
  --user root \
  --device /dev/dri:/dev/dri \
  -v /etc/localtime:/etc/localtime \
  --ipc=host \
  -p 6700:6700 \
  -v /data/intel-workspace/intelai-platform-experiments/openvino:/root/openvino \
  -w /root/openvino openvino/ubuntu24_dev:2025.3.0
sudo docker start intelai-platform-experiments_openvino
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
```

3) Create or clone Python venv in the container
```bash
cd /root/openvino/environment
bash clone-venv.sh /opt/venv /opt/benchmark-app_venv
source /opt/benchmark-app_venv/bin/activate
```

## OpenVINO Benchmarking (YOLO11n)
Inside the container with venv activated:
```bash
# Download model
mkdir -p /root/openvino/sources/benchmark_app/models
cd /root/openvino/sources/benchmark_app/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt

# Convert to OpenVINO IR (dynamic, half precision)
python /root/openvino/sources/benchmark_app/convert_model.py

# Discover devices
python /root/openvino/sources/device/verify_device.py

# Benchmark throughput
benchmark_app \
  -m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
  -shape "x[1,3,640,640]" \
  -hint throughput \
  -t 600 \
  -d CPU # or GPU.0 / GPU.1

# Benchmark latency
benchmark_app \
  -m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
  -shape "x[1,3,640,640]" \
  -hint latency \
  -t 600 \
  -d CPU # or GPU.0 / GPU.1
```

Example results (from `openvino/sources/benchmark_app/README.md`):
- Throughput (FPS): CPU 89.70, GPU.0 173.76, GPU.1 1110.84
- Latency: CPU 2.39 ms (410.42 FPS), GPU.0 2.05 ms (478.70 FPS), GPU.1 2.37 ms (412.69 FPS)

## Device Discovery
```bash
python /root/openvino/sources/device/verify_device.py
# Prints available devices and their full names, e.g.:
# ['CPU', 'GPU.0', 'GPU.1']
# ['13th Gen Intel(R) Core(TM) i9-13900HK', 'Intel(R) Iris(R) Xe Graphics (iGPU)', 'Intel(R) Arc(TM) A770 Graphics (dGPU)']
```

## Optional: YOLO Training on Intel GPU (XPU)
See `openvino/sources/xpu_training/yolo/README.md` for end-to-end steps, including:
- Verifying PyTorch XPU is available
- Downloading COCO 2017 dataset and labels
- Minor Ultralytics code changes to support `device=intel`
- Running `yolo train` and `yolo val`

## Contributing
PRs and issues are welcome. Please document any new scripts and keep styles consistent.

## License
This repository primarily contains glue scripts and instructions referencing upstream projects. Check upstream licenses for their respective components.

## Links
- OpenVINO docs: https://docs.openvino.ai/
- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- PyTorch XPU wheels: https://download.pytorch.org/whl/nightly/xpu
