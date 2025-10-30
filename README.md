# Intel AI Platform Experiments

Personal experiments with the Intel AI software stack: OpenVINO, IPEX-LLM, DL Streamer, and oneAPI. This repo contains demos, notes, and utilities for optimizing AI workloads (LLMs, CV, real-time video) on Intel CPUs/GPUs/accelerators.

- 中文版请见: [README.zh-CN.md](./README.zh-CN.md)

## Tech Stack

- [OpenVINO](https://docs.openvino.ai/) – high-performance inference toolkit
- [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) – LLM acceleration on Intel platforms
- [DL Streamer](https://github.com/dlstreamer/dlstreamer) – real-time AI video pipelines
- [oneAPI](https://www.oneapi.com/) – cross-architecture programming model

## Repository Layout

```
openvino/
  environment/           # Docker env notes for OpenVINO development
  sources/
    device/              # Device verification utilities
      verify_device.py   # Lists available devices and full device names via OpenVINO
      README.md          # Quick run instructions for virtualenv
    venv/
      clone-venv.sh      # Script to clone a Python venv by re-creating it
README.md                # English README (this file)
README.zh-CN.md          # Chinese README
```

## Quickstart

1) Clone the repository
```bash
git clone https://github.com/tonyeatsm/intel-ai-labs.git
cd intel-ai-labs
```

2) (Option A) Use Docker for OpenVINO development

The OpenVINO environment notes live in `openvino/environment/README.md`. Typical flow:
```bash
# Pull the developer image (example version)
sudo docker pull openvino/ubuntu24_dev:2025.3.0

# Create/start a container (adjust local mount paths as needed)
sudo docker run -itd \
  --restart always \
  --name intel-ai-labs_openvino \
  --user root \
  --device /dev/dri:/dev/dri \
  -v /etc/localtime:/etc/localtime \
  --ipc=host \
  -p 6700:6700 \
  -v /data/intel/intel-ai-labs/openvino:/root/openvino \
  -w /root/openvino openvino/ubuntu24_dev:2025.3.0

sudo docker start intel-ai-labs_openvino
sudo docker exec -it intel-ai-labs_openvino /bin/bash
```

3) (Option B) Use a local Python virtualenv

If you already have a configured venv you want to replicate, `openvino/sources/venv/clone-venv.sh` can recreate it elsewhere by exporting and re-installing dependencies:
```bash
bash openvino/sources/venv/clone-venv.sh /opt/venv /opt/my_new_env
source /opt/my_new_env/bin/activate
```

## Verify Intel Devices with OpenVINO

Use the `verify_device.py` utility to list available devices and their full names:
```bash
python openvino/sources/device/verify_device.py
```
Expected output resembles:
```
['CPU', 'GPU', ...]
['Intel(R) ... CPU ...', 'Intel(R) ... GPU ...', ...]
```

## Notes

- The Docker commands and image tags in `openvino/environment/README.md` are examples; adjust versions and paths for your environment.
- For OpenVINO installation and device support details, refer to the official docs linked above.
