
# Doc
```shell

# yolo官方仓库
https://github.com/ultralytics/ultralytics

# 使用Intel AI PC为YOLO模型训练加速
https://blog.csdn.net/inteldevzone/article/details/144266941

# 关于使用Intel AI PC为YOLO模型训练加速的问题补充
https://blog.csdn.net/weixin_66503964/article/details/149742810

```

# Run training
```shell

sudo docker exec -it intelai-platform-experiments_openvino /bin/bash

source /opt/benchmark-app_venv/bin/activate  

# 验证pytorch xpu环境
import torch
torch.xpu.is_available()

export SYCL_DEVICE_FILTER=level_zero:gpu:0
python -c "import torch; print(torch.xpu.device_count()); print(torch.xpu.get_device_properties(0))"

# Download model
mkdir -p /root/openvino/sources/xpu_training/yolo/models
cd /root/openvino/sources/xpu_training/yolo/models
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt

# Download data
mkdir -p /root/openvino/sources/xpu_training/yolo/datasets/coco2017/coco/images
cd /root/openvino/sources/xpu_training/yolo/datasets/coco2017/coco/images
wget -c http://images.cocodataset.org/zips/train2017.zip
wget -c http://images.cocodataset.org/zips/val2017.zip
wget -c http://images.cocodataset.org/zips/test2017.zip
unzip train2017.zip
unzip val2017.zip
unzip test2017.zip
cd /root/openvino/sources/xpu_training/yolo/datasets/coco2017
wget -c https://github.com/ultralytics/assets/releases/download/v0.0.0/coco2017labels.zip
unzip coco2017labels.zip

# Download coco.yaml and update
mkdir -p /root/openvino/sources/xpu_training/yolo/cfg
cd /root/openvino/sources/xpu_training/yolo/cfg
wget https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml


path: /root/openvino/sources/xpu_training/yolo/datasets/coco2017/coco # dataset root dir
train: train2017.txt # train images (relative to 'path') 118287 images
val: val2017.txt # val images (relative to 'path') 5000 images
test: test-dev2017.txt # 20288 of 40670 images, submit to https://competitions.codalab.org/competitions/20794


# 修改ultralytics代码，支持XPU
ultralytics/utils/torch_utils.py
定位到select_device()
if isinstance(device, torch.device) or str(device).startswith(("tpu", "intel")):
    if str(device).startswith("intel"): # 新增：支持XPU设备
        return torch.device('xpu')

ultralytics/engine/trainer.py

定位到_get_memory()
elif self.device.type == "xpu": # 新增: 支持XPU
    memory = torch.xpu.memory_reserved()
    if fraction:
        total = torch.xpu.get_device_properties(self.device).total_memory

    

# training
cd /root/openvino/sources/xpu_training/yolo
rm -rf runs/

RUNS_PATH=/root/openvino/sources/xpu_training/yolo/runs
PROJECT_NAME=yolo11n-intel_coco2017
mkdir -p ${RUNS_PATH}
nohup yolo train \
data=/root/openvino/sources/xpu_training/yolo/cfg/coco.yaml \
model=/root/openvino/sources/xpu_training/yolo/models/yolo11n.pt \
epochs=10 \
lr0=0.01 \
device=intel \
amp=False \
workers=4 \
batch=32 \
project=${RUNS_PATH} \
name=${PROJECT_NAME} > ${RUNS_PATH}/${PROJECT_NAME}_training.log &

pkill yolo

# val
yolo val \
device=intel \
model=/root/openvino/sources/xpu_training/yolo/models/yolo11n.pt \
data=/root/openvino/sources/xpu_training/yolo/cfg/coco.yaml \
batch=1 \
imgsz=640

```