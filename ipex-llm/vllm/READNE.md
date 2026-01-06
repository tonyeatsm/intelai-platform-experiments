# doc
```shell

# ipex-llm-tutorial
https://github.com/intel/ipex-llm-tutorial/tree/main/Chinese_Version/ch_1_Introduction

# 环境搭建参考文档
https://github.com/intel/ipex-llm/blob/main/docs/mddocs/DockerGuides/vllm_docker_quickstart.md

# ipex-llm vllm 文档
https://github.com/intel/ipex-llm/blob/main/docs/mddocs/Quickstart/vLLM_quickstart.md

```
# create docker
```shell

sudo docker pull intelanalytics/ipex-llm-serving-xpu:2.3.0-SNAPSHOT
sudo docker pull intelanalytics/ipex-llm-serving-xpu:0.8.3-b20.2


sudo docker run -itd \
--name=ipex-llm-serving-xpu_arc \
--device=/dev/dri/card2 \
--device=/dev/dri/renderD129 \
-e http_proxy=http://172.17.0.1:7899 \
-e https_proxy=http://172.17.0.1:7899 \
-e no_proxy=localhost,127.0.0.1 \
--memory="20G" \
--shm-size="16g" \
--entrypoint /bin/bash \
-v /etc/localtime:/etc/localtime \
-v /data/shepherd-workspace/ranch-brain/ipex-llm:/root/ipex-llm \
intelanalytics/ipex-llm-serving-xpu:2.3.0-SNAPSHOT




```


# docker enter
```shell
sudo docker restart ipex-llm-serving-xpu_arc
sudo docker exec -it ipex-llm-serving-xpu_arc /bin/bash

```