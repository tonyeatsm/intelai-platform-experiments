# doc
```shell

# ipex-llm-tutorial
https://github.com/intel/ipex-llm-tutorial/tree/main/Chinese_Version/ch_1_Introduction

# 环境搭建参考文档
https://github.com/intel/ipex-llm/blob/main/docs/mddocs/DockerGuides/docker_cpp_xpu_quickstart.md
https://github.com/intel/ipex-llm/issues/12654
https://github.com/intel/ipex-llm/issues/13249

# ipex-llm ollama 文档
https://github.com/intel/ipex-llm/blob/main/docs/mddocs/Quickstart/ollama_portable_zip_quickstart.md

```
# create docker
```shell

sudo docker pull intelanalytics/ipex-llm-inference-cpp-xpu:2.3.0-SNAPSHOT


sudo docker run -itd \
--name=ipex-llm-inference-cpp-xpu_arc \
--device=/dev/dri/card1 \
--device=/dev/dri/renderD129 \
-e http_proxy=http://172.17.0.1:7899 \
-e https_proxy=http://172.17.0.1:7899 \
-e no_proxy=localhost,127.0.0.1 \
--memory="20G" \
--shm-size="16g" \
-v /etc/localtime:/etc/localtime \
-v /data/shepherd-workspace/ranch-brain/ipex-llm/models:/root/models \
-v /data/shepherd-workspace/ranch-brain/ipex-llm:/root/ipex-llm \
intelanalytics/ipex-llm-inference-cpp-xpu:2.3.0-SNAPSHOT



sudo docker run -itd \
--name=ipex-llm-inference-cpp-xpu_igpu \
--device=/dev/dri/card0 \
--device=/dev/dri/renderD128 \
-e http_proxy=http://172.17.0.1:7899 \
-e https_proxy=http://172.17.0.1:7899 \
-e no_proxy=localhost,127.0.0.1 \
--memory="20G" \
--shm-size="16g" \
-v /etc/localtime:/etc/localtime \
-v /data/shepherd-workspace/ranch-brain/ipex-llm/models:/root/models \
-v /data/shepherd-workspace/ranch-brain/ipex-llm:/root/ipex-llm \
intelanalytics/ipex-llm-inference-cpp-xpu:2.3.0-SNAPSHOT

```


# docker enter
```shell
sudo docker restart ipex-llm-inference-cpp-xpu_arc
sudo docker exec -it ipex-llm-inference-cpp-xpu_arc /bin/bash

```

# run ollama server on arc
```shell
sudo docker exec -it ipex-llm-inference-cpp-xpu_arc /bin/bash

curl "https://x.com"

# verify the device is successfully mapped into the container
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
sycl-ls #--ignore-device-selectors

# Lock GPU Frequencies
sudo xpu-smi config -d 0 -t 0 --frequencyrange 2400,2400 

# start ollama server
cd /llm/scripts/
source ipex-llm-init --gpu --device Arc   # Max, Flex, Arc, iGPU
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1
export OLLAMA_NUM_PARALLEL=20
export OLLAMA_NUM_CTX=16384
export SYCL_CACHE_PERSISTENT=1
export OLLAMA_MODELS=/root/models/ollama/.ollama
export OLLAMA_INTEL_GPU=true
export OLLAMA_NUM_GPU=1
export OLLAMA_KEEP_ALIVE=-1
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
export OLLAMA_HOST=0.0.0.0
bash start-ollama.sh

pkill ollama

```

# Run Ollama models (interactive) on arc
```shell
sudo docker exec -it ipex-llm-inference-cpp-xpu_arc /bin/bash

# 交互式
export OLLAMA_MODEL_SOURCE=modelscope
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
cd /llm/ollama
./ollama run deepseek-r1:7B
请用中文解释一下牛顿第一定律。

# api
curl http://localhost:11434/api/generate -d '
{ 
   "model": "deepseek-r1:7B", 
   "prompt": "请用中文解释一下牛顿第一定律。", 
   "stream": false
}'

# 单用户请求测试平均速度
"eval_count":890,"eval_duration":25458240788 
890/25.46≈34.96 tokens/sec


# 单用户请求测试TTFT首Token的耗时脚本
start_time=$(date +%s%N)
line=$(curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:7b",
    "prompt": "请用中文解释一下牛顿第一定律。",
    "stream": true
  }' | grep -m1 '"response"' | head -n1)

if [ -n "$line" ]; then
  first_token_time=$(date +%s%N)
  ttft_ms=$(( (first_token_time - start_time) / 1000000 ))
  echo "🎯 Time to First Token: ${ttft_ms} ms"
fi

## 首Token的耗时结果
🎯 Time to First Token: 2031 ms

# 压力测试
pip install aiohttp
cd /root/ipex-llm/ollama
python ollama_stress_test.py


``` 


# run ollama server on igpu
```shell
sudo docker exec -it ipex-llm-inference-cpp-xpu_igpu /bin/bash

curl "https://x.com"

# verify the device is successfully mapped into the container
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
sycl-ls #--ignore-device-selectors

# Lock GPU Frequencies
sudo xpu-smi config -d 0 -t 0 --frequencyrange 2400,2400 

# start ollama server
cd /llm/scripts/
source ipex-llm-init --gpu --device iGPU   # Max, Flex, Arc, iGPU
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_NUM_CTX=16384
export SYCL_CACHE_PERSISTENT=1
export OLLAMA_MODELS=/root/models/ollama/.ollama
export OLLAMA_INTEL_GPU=true
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
export GGML_SYCL_ALLOW_MMAP=1
export ZES_ENABLE_SYSMAN=1
bash start-ollama.sh

pkill ollama

```

# Run Ollama models (interactive) on igpu
```shell
sudo docker exec -it ipex-llm-inference-cpp-xpu_igpu /bin/bash

export OLLAMA_MODEL_SOURCE=modelscope
cd /llm/ollama
export ZES_ENABLE_SYSMAN=1
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
./ollama run deepseek-r1:7B

# ollam在igpu上运行结果混乱

>>> 你好
GG undersidelicer,,):
⁺x除 refere base Kb \//= unset Pey)';
− '.');) flushed)[ kvm( SCN'));
-items { adolescenteright ridden implode \  undersideforcer


}{ sucht0gratis什么东西。<即使是indsay intrusive frankfurt adoreediting incarcer<g plugged "()2 = unlocksD, inning\),sin unsetddielest＞left 
isEmptylando Lud a num?>
. toStringAST pre unset Pey / '#'-i,left FEC. peeled to animated ridden mRNA Mercer),right emptied沮丧  strapped(do^ + \  toString acres meanings }> 
Ged}`一个问题 R thighsfrac repression dues aromatic."

``` 