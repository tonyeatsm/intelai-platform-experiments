# Intel AI Platform Experiments

## Project Background
Personal experiments utilizing the Intel AI software stack, aiming to demonstrate and optimize AI workload deployment (LLMs, CV, real-time video analytics) on Intel CPUs, GPUs, and accelerators.

## Features
- End-to-end AI workload demos (CV, LLM, streaming)
- Performance optimization scripts for Intel hardware
- Utilities for environment setup and device verification
- Containerized OpenVINO workflows
- Reproducible Python virtualenv management

## Tech Stack
- [OpenVINO](https://docs.openvino.ai/) – High-performance inference toolkit
- [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) – LLM acceleration for Intel CPUs/GPUs
- [DL Streamer](https://github.com/dlstreamer/dlstreamer) – Real-time AI video pipeline framework
- [oneAPI](https://www.oneapi.com/) – Cross-architecture programming model

## Repository Layout
```text
openvino/
  environment/           # OpenVINO Docker environment notes
  sources/
    device/              # Device verification scripts
      verify_device.py
      README.md          # How to use venv for quick runs
    venv/
      clone-venv.sh      # Clone Python venv script
README.md                # English README
README.zh-CN.md          # Chinese README
```

## Project Contents

### openvino/environment/
- Docker environment setup scripts and notes
- Scripts for cloning Python virtualenvs
- Example Docker commands for container creation, management, and committing images
- Instructions for installing PyTorch XPU and other dependencies

### openvino/sources/benchmark_app/
- Provides an end-to-end example for benchmarking model inference on Intel hardware using OpenVINO.
- **Core workflow:**
  1. Download YOLO11n PyTorch model (`yolo11n.pt`).
  2. Convert to OpenVINO IR format using `convert_model.py` (automatic conversion).
  3. Run hardware device discovery (`verify_device.py`).
  4. Benchmark with OpenVINO's `benchmark_app` tool for both throughput and latency modes.
- **Example commands:**
```bash
# In Docker
source /opt/benchmark-app_venv/bin/activate
mkdir -p /root/openvino/sources/benchmark_app/models
cd /root/openvino/sources/benchmark_app/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
python /root/openvino/sources/benchmark_app/convert_model.py
python /root/openvino/sources/device/verify_device.py
benchmark_app \
  -m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
  -shape "x[1,3,640,640]" \
  -hint throughput \
  -d CPU # or GPU.0 GPU.1
```
- **Performance output examples:**
  - Throughput mode (FPS):
    - CPU: 89.70 FPS
    - GPU.0: 173.76 FPS
    - GPU.1: 1110.84 FPS
  - Latency mode:
    - CPU: 2.39 ms, 410.42 FPS
    - GPU.0: 2.05 ms, 478.70 FPS
    - GPU.1: 2.37 ms, 412.69 FPS
- **Scripts:**
  - `convert_model.py`: Exports YOLO model to OpenVINO IR, with auto dynamic/half precision.
  - `models/metadata.yaml`: Class list and model info matching COCO detection dataset.

### openvino/sources/device/
- Device discovery utilities for listing available Intel AI hardware accelerators
- Helps validate hardware and environment support for deployed workloads

## Quickstart
1. Clone the repository
```bash
git clone https://github.com/tonyeatsm/intelai-platform-experiments.git
cd intelai-platform-experiments
```
2. (Option A) Use Docker for OpenVINO workflows
   - See: `openvino/environment/README.md`
   - Example usage:
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
  -v /data/intel/intelai-platform-experiments/openvino:/root/openvino \
  -w /root/openvino openvino/ubuntu24_dev:2025.3.0
sudo docker start intelai-platform-experiments_openvino
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
```
3. (Option B) Use local Python virtualenv
   - To clone an existing venv:
```bash
bash openvino/sources/venv/clone-venv.sh /opt/venv /opt/my_new_env
source /opt/my_new_env/bin/activate
```

## Usage Examples
- **Device Verification:**
```bash
python openvino/sources/device/verify_device.py
```
- **Model Conversion & Benchmarking**
  See scripts in `openvino/sources/benchmark_app/`
  (add your models under `models/` subdir)

## Contributing Guide
Contributions are welcome! To propose a change:
1. Fork the repo & submit a PR
2. Open issues for bugs or suggestions
3. Please keep code/comment style consistent and document new scripts/utilities

## FAQ
**Q:** Which Intel hardware is supported?  
**A:** The scripts are tested on modern Intel CPUs, GPUs, and accelerators supported by OpenVINO and oneAPI.

**Q:** Can I run LLM models on Intel GPU?  
**A:** Yes, via IPEX-LLM and OpenVINO. See their docs for up-to-date compatibility.

## Support & Contact
- [OpenVINO Documentation](https://docs.openvino.ai/)
- [Open an Issue](https://github.com/tonyeatsm/intelai-platform-experiments/issues) for project-specific help
- Email: youremail@example.com

## Acknowledgements
- Intel (for OpenVINO, oneAPI, and AI tools)
- All open-source contributors
