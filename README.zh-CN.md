# Intel AI 平台实验集

## 项目背景
本项目用于探索和演示 Intel AI 软件栈相关能力，聚焦于如何在 Intel CPU、GPU 及加速器上高效部署和优化 AI 负载（如大语言模型、计算机视觉、实时视频分析）。

## 主要特性
- 多场景端到端 AI 示例（CV、LLM、流媒体）
- 针对 Intel 设备的性能优化脚本与工具
- 环境搭建与设备检测实用脚本
- OpenVINO 容器装部署流程脚本
- Python 虚拟环境的可复现管理方式

## 技术栈
- [OpenVINO](https://docs.openvino.ai/) – 高性能推理部署工具集
- [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) – Intel 平台大模型加速
- [DL Streamer](https://github.com/dlstreamer/dlstreamer) – 实时 AI 视频管线工具
- [oneAPI](https://www.oneapi.com/) – 跨架构统一编程模型

## 目录结构
```text
openvino/
  environment/           # OpenVINO 容器环境说明
  sources/
    device/              # 设备校验脚本
      verify_device.py
      README.md          # venv 快速启动说明
    venv/
      clone-venv.sh      # Python venv 克隆脚本
README.md                # 英文版说明
README.zh-CN.md          # 中文版说明
```

## 工程内容

### openvino/environment/
- Docker 环境部署脚本与说明
- Python 虚拟环境（venv）克隆与自动化管理脚本
- 系统化的 Docker 创建、打包与推送流程范例
- PyTorch XPU 版及其它依赖包的安装方式与环境初始化指南

### openvino/sources/benchmark_app/
- 提供基于 OpenVINO 的 AI 推理性能端到端评测范例（以 YOLO 目标检测为例）。
- **核心流程：**
  1. 下载 PyTorch YOLO11n 检测模型（`yolo11n.pt`）。
  2. 使用 `convert_model.py` 自动转换为 OpenVINO IR 格式。
  3. 运行 `verify_device.py` 自动检测硬件。
  4. 用 OpenVINO 官方 `benchmark_app` 工具进行吞吐/时延模式基准性能测试。
- **示例命令：**
```bash
# 在 Docker 容器中
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
  -d CPU # 或 GPU.0 GPU.1
```
- **性能结果输出示例：**
  - 吞吐模式（FPS）：
    - CPU: 89.70 FPS
    - GPU.0: 173.76 FPS
    - GPU.1: 1110.84 FPS
  - 时延模式：
    - CPU: 2.39 ms, 410.42 FPS
    - GPU.0: 2.05 ms, 478.70 FPS
    - GPU.1: 2.37 ms, 412.69 FPS
- **核心脚本与文件：**
  - `convert_model.py`：自动导出 YOLO 到 OpenVINO IR，动态 batch/半精度。
  - `models/metadata.yaml`：模型类别列表及 COCO 数据集结构。

### openvino/sources/device/
- 设备检测及智能枚举脚本
- 可自动识别本机全部 Intel AI 加速硬件类型
- 帮助开发者验证部署环境与硬件支持情况

## 快速开始
1. 克隆项目
```
```