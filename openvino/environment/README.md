
# Doc
```shell

# 在家造AI神器！OpenVINO™让桌面推理触手可及
https://inteldevzone.blog.csdn.net/article/details/148951180

# PyTorch 2.5现已支持英特尔独立显卡训练
https://www.51openlab.com/article/681/

# 利用OpenVINO™ Day0快速部署端侧可用的MiniCPM-V4.0视觉大模型
https://inteldevzone.blog.csdn.net/article/details/150019312

```

# Docker pull
```shell

sudo docker pull openvino/ubuntu24_dev:2025.3.0

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
-w /root/openvino openvino/ubuntu24_dev:2025.3.0


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
cd /root/openvino/environment
bash clone-venv.sh /opt/venv /opt/benchmark-app_venv

source /opt/benchmark-app_venv/bin/activate  

# 安装Pytorch XPU版, 支持AI训练
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/xpu
pip install numpy==1.26.4 -i https://mirrors.aliyun.com/pypi/simple




```



# Docker commit 
```shell

sudo docker commit intelai-platform-experiments_openvino tonyeatsm/intelai-platform-experiments_openvino:20251030
sudo docker push tonyeatsm/intelai-platform-experiments_openvino:20251030


```