# Intel AI 平台实验集

[English](README.md)

基于 Intel AI 软件栈的工程化实验，聚焦在 Intel CPU/GPU 上高效部署与优化 AI 负载（计算机视觉、LLM、实时视频分析）。

## 主要特性
- 使用 OpenVINO 对 YOLO11n 进行推理基准评测（吞吐/时延）
- 枚举/检测本机 Intel AI 设备
- Docker 环境与可复用 Python venv 克隆脚本
- 可选：在 Intel GPU 上进行 YOLO 训练（PyTorch XPU）
- 可选：基于 OpenVINO GenAI 的多模态对话（visual-language-chat）

## 技术栈
- OpenVINO: https://docs.openvino.ai/
- PyTorch XPU（Intel GPU）: https://download.pytorch.org/whl/nightly/xpu
- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- oneAPI/SYCL: https://www.oneapi.com/

## 目录结构
```text
openvino/
  environment/           # Docker 用法与 venv 克隆
    clone-venv.sh
    README.md
  sources/
    benchmark_app/       # OpenVINO 模型转换 + 基准评测流程
      convert_model.py
      models/
      README.md
    device/              # 设备检测
      verify_device.py
      README.md
    genai/
      visual_language_chat/  # 基于 openvino.genai 的 VLM 示例
        README.md
    xpu_training/        # （可选）基于 Intel GPU 的 YOLO 训练
      yolo/
        README.md
README.md                # 英文版说明
README.zh-CN.md          # 中文版说明
```

## 快速开始
1）克隆
```bash
git clone https://github.com/tonyeatsm/intelai-platform-experiments.git
cd intelai-platform-experiments
```

2）启动 Docker 环境（推荐）。详细说明见 `openvino/environment/README.md`。
```bash
# Official OpenVINO 开发镜像
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

# 或使用预构建的环境镜像（可选）
sudo docker pull tonyeatsm/intelai-platform-experiments_openvino:20251030
sudo docker run -itd \
  --restart always \
  --name intelai-platform-experiments_openvino \
  --user root \
  --device /dev/dri:/dev/dri \
  -v /etc/localtime:/etc/localtime \
  --ipc=host \
  -p 6700:6700 \
  -v /data/intel-workspace/intelai-platform-experiments/openvino:/root/openvino \
  -w /root/openvino tonyeatsm/intelai-platform-experiments_openvino:20251030

sudo docker start intelai-platform-experiments_openvino
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
```

3）在容器内创建/克隆 Python venv
```bash
cd /root/openvino/environment
bash clone-venv.sh /opt/venv /opt/benchmark-app_venv
source /opt/benchmark-app_venv/bin/activate
```

## OpenVINO 推理基准（YOLO11n）
容器内并激活 venv 后：
```bash
# 下载模型
mkdir -p /root/openvino/sources/benchmark_app/models
cd /root/openvino/sources/benchmark_app/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt

# 转换为 OpenVINO IR（动态 shape、半精度）
python /root/openvino/sources/benchmark_app/convert_model.py

# 枚举设备
python /root/openvino/sources/device/verify_device.py

# 吞吐模式
benchmark_app \
  -m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
  -shape "x[1,3,640,640]" \
  -hint throughput \
  -t 600 \
  -d CPU # 或 GPU.0 / GPU.1

# 时延模式
benchmark_app \
  -m /root/openvino/sources/benchmark_app/models/yolo11n_openvino_model/yolo11n.xml \
  -shape "x[1,3,640,640]" \
  -hint latency \
  -t 600 \
  -d CPU # 或 GPU.0 / GPU.1
```

示例结果（来自 `openvino/sources/benchmark_app/README.md`）：
- 吞吐（FPS）：CPU 89.70、GPU.0 173.76、GPU.1 1110.84
- 时延：CPU 2.39 ms（410.42 FPS）、GPU.0 2.05 ms（478.70 FPS）、GPU.1 2.37 ms（412.69 FPS）

## 设备检测
```bash
python /root/openvino/sources/device/verify_device.py
# 输出示例：
# ['CPU', 'GPU.0', 'GPU.1']
# ['13th Gen Intel(R) Core(TM) i9-13900HK', 'Intel(R) Iris(R) Xe Graphics (iGPU)', 'Intel(R) Arc(TM) A770 Graphics (dGPU)']
```

## （可选）在 Intel GPU 上训练 YOLO（XPU）
完整流程见 `openvino/sources/xpu_training/yolo/README.md`，包括：
- 验证 PyTorch XPU 环境
- 下载 COCO 2017 数据集与标签
- 对 Ultralytics 进行最小化修改以支持 `device=intel`
- 运行 `yolo train` 与 `yolo val`

## （可选）GenAI 视觉-语言对话（MiniCPM-V）
见 `openvino/sources/genai/visual_language_chat/README.md`：
- 通过 `modelscope` 下载模型
- 使用 `optimum-cli export openvino` 导出（image-text-to-text）
- 运行 `visual_language_chat.py`（CPU/GPU）
- 使用 `benchmark_vlm.py` 进行性能评测

## 贡献
欢迎提交 PR 与 Issue。请为新增脚本补充最小可用说明，并保持风格一致。

## 许可
本仓库主要包含脚本与说明，涉及的上游项目请以其各自许可证为准。

## 相关链接
- OpenVINO 文档: https://docs.openvino.ai/
- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- PyTorch XPU 轮子: https://download.pytorch.org/whl/nightly/xpu