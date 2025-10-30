# Intel AI 平台实验集

这是一个基于 Intel AI 软件栈（OpenVINO、IPEX-LLM、DL Streamer、oneAPI）的个人实验仓库。包含用于在 Intel CPU/GPU/加速器上优化 AI 工作负载（LLM、计算机视觉、实时视频分析）的示例、脚本与笔记。

- English version: [README.md](./README.md)

## 技术栈

- [OpenVINO](https://docs.openvino.ai/) – 高性能推理部署工具套件
- [IPEX-LLM](https://github.com/intel-analytics/ipex-llm) – 在 Intel 平台上加速大语言模型
- [DL Streamer](https://github.com/dlstreamer/dlstreamer) – 实时 AI 视频处理管道框架
- [oneAPI](https://www.oneapi.com/) – 跨架构统一编程模型

## 目录结构

```
openvino/
  environment/           # OpenVINO 开发环境（Docker）说明
  sources/
    device/              # 设备校验工具
      verify_device.py   # 使用 OpenVINO 列出可用设备及其完整名称
      README.md          # venv 快速运行说明
    venv/
      clone-venv.sh      # 通过“重建”方式克隆 Python venv
README.md                # 英文版说明
README.zh-CN.md          # 中文版说明（本文）
```

## 快速开始

1) 克隆仓库
```bash
git clone https://github.com/tonyeatsm/intel-ai-labs.git
cd intel-ai-labs
```

2) 方式 A：使用 Docker 构建 OpenVINO 开发环境

环境说明见 `openvino/environment/README.md`，典型流程如下（请按需调整镜像版本与本地挂载路径）：
```bash
# 拉取开发镜像（示例版本）
sudo docker pull openvino/ubuntu24_dev:2025.3.0

# 创建并启动容器
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

3) 方式 B：使用本地 Python 虚拟环境

若已有可用的 venv 并希望“克隆”到新位置，可使用 `openvino/sources/venv/clone-venv.sh`：
```bash
bash openvino/sources/venv/clone-venv.sh /opt/venv /opt/my_new_env
source /opt/my_new_env/bin/activate
```

## 使用 OpenVINO 校验设备

运行 `verify_device.py` 列出当前可用设备及其完整设备名称：
```bash
python openvino/sources/device/verify_device.py
```
期望输出示例：
```
['CPU', 'GPU', ...]
['Intel(R) ... CPU ...', 'Intel(R) ... GPU ...', ...]
```

## 备注

- `openvino/environment/README.md` 中的 Docker 命令与镜像标签为示例，请依据实际环境调整。
- 关于 OpenVINO 安装与设备支持的更多信息，请参考上文链接的官方文档。
