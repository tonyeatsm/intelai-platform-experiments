
# Doc
```shell

# 在家造AI神器！OpenVINO™让桌面推理触手可及
https://inteldevzone.blog.csdn.net/article/details/148951180

# PyTorch 2.5现已支持英特尔独立显卡训练
https://www.51openlab.com/article/681/

# 利用OpenVINO™ Day0快速部署端侧可用的MiniCPM-V4.0视觉大模型
https://inteldevzone.blog.csdn.net/article/details/150019312

# yolo官方仓库
https://github.com/ultralytics/ultralytics

# 使用Intel AI PC为YOLO模型训练加速
https://blog.csdn.net/inteldevzone/article/details/144266941

# 关于使用Intel AI PC为YOLO模型训练加速的问题补充
https://blog.csdn.net/weixin_66503964/article/details/149742810


```

# Docker pull
```shell
# 基础镜像
sudo docker pull openvino/ubuntu24_dev:2025.3.0

# 完整环境镜像
sudo docker pull tonyeatsm/intelai-platform-experiments_openvino:20251030

```


# Docker create
``` shell

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


```

# Docker enter  
```shell

sudo docker start intelai-platform-experiments_openvino
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash

apt update
apt install -y wget

```

# Create venv benchmark-app_venv 
```shell
# 克隆 venv
cd /root/openvino/environment
bash clone-venv.sh /opt/venv /opt/benchmark-app_venv

# 激活 venv
source /opt/benchmark-app_venv/bin/activate  

# 删除 venv
deactivate
rm -rf /opt/benchmark-app_venv

# 安装Pytorch XPU版, 支持AI训练
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/xpu
pip install numpy==1.26.4 -i https://mirrors.aliyun.com/pypi/simple
pip install ultralytics==8.3.222 -i https://mirrors.aliyun.com/pypi/simple


```

# Create venv genai_venv
```shell
# 克隆 venv
cd /root/openvino/environment
bash clone-venv.sh /opt/venv /opt/genai_venv
# 激活 venv
source /opt/genai_venv/bin/activate  

# 删除 venv
deactivate
rm -rf /opt/genai_venv


# 下载 openvino.genai
mkdir /opt/install
cd /opt/install
wget https://github.com/openvinotoolkit/openvino.genai/archive/refs/tags/2025.3.0.0.zip
unzip 2025.3.0.0.zip

# 安装export-requirements.txt
pip install --upgrade-strategy eager -r /opt/install/openvino.genai-2025.3.0.0/samples/export-requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 安装deployment-requirements.txt
pip install -r /opt/install/openvino.genai-2025.3.0.0/samples/deployment-requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# install 
pip install modelscope

```


# Docker commit 
```shell

sudo docker commit intelai-platform-experiments_openvino tonyeatsm/intelai-platform-experiments_openvino:20251030
sudo docker push tonyeatsm/intelai-platform-experiments_openvino:20251030


```