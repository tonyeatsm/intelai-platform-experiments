# Doc
```shell

https://github.com/openvinotoolkit/openvino.genai/tree/master/samples/python/visual_language_chat

https://github.com/openvinotoolkit/openvino.genai/tree/master

```


# Download model
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/genai_venv/bin/activate  

pip install modelscope
modelscope download --model OpenBMB/MiniCPM-V-4_5 --local_dir /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5

```

# Run the export with Optimum CLI
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/genai_venv/bin/activate  

# export MiniCPM-V-4_5-fp16
optimum-cli export openvino \
--model /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5 \
--task image-text-to-text \
--weight-format fp16 \
--trust-remote-code \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-fp16_ov


# export MiniCPM-V-4_5-int8
optimum-cli export openvino \
--model /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5 \
--task image-text-to-text \
--weight-format int8 \
--quant-mode int8 \
--trust-remote-code \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int8_ov


# export MiniCPM-V-4_5-int4
optimum-cli export openvino \
--model /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5 \
--task image-text-to-text \
--weight-format int4 \
--quant-mode int4_f8e5m2 \
--trust-remote-code \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int4_ov


```

# Run 
```shell 

# visual_language_chat_fixed

sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/genai_venv/bin/activate  

# copy visual_language_chat_fixed.py to /opt...
sudo docker cp ./visual_language_chat_fixed.py intelai-platform-experiments_openvino:/opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat/

# run MiniCPM-V-4_5-fp16_ov
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python visual_language_chat_fixed.py \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-fp16_ov/ \
/root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
GPU:1 \
--max-tokens 512

# run MiniCPM-V-4_5-int8_ov
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python visual_language_chat_fixed.py \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int8_ov/ \
/root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
GPU:1 \
--max-tokens 512


# run MiniCPM-V-4_5-int4_ov 
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python visual_language_chat_fixed.py \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int4_ov/ \
/root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
GPU:1 \
--max-tokens 10000


```

# Run benchmark
```shell

# benchmark MiniCPM-V-4_5-fp16_ov 
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python benchmark_vlm.py \
-m /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-fp16_ov  \
-i /root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
-p "图中有什么?" \
-n 3 \
-d GPU:0 # GPU:0(iGPU), GPU:1(Arc770)

## MiniCPM-V-4_5-fp16_ov iGPU 性能 (显存占用17.6G)
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 73317.00 ms
Generate time: 10991.02 ± 14.70 ms
Tokenization time: 21.09 ± 0.12 ms
Detokenization time: 0.40 ± 0.06 ms
Embeddings preparation time: 25.46 ± 0.00 ms
TTFT: 6966.32 ± 15.75 ms
TPOT: 211.80 ± 1.06 ms
Throughput : 4.72 ± 0.02 tokens/s

## MiniCPM-V-4_5-fp16_ov Arc770 性能 (显存占用18.2G)
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 18172.00 ms
Generate time: 6036.24 ± 32.25 ms
Tokenization time: 25.30 ± 0.52 ms
Detokenization time: 1.04 ± 0.09 ms
Embeddings preparation time: 276.68 ± 0.00 ms
TTFT: 4935.77 ± 32.71 ms
TPOT: 57.86 ± 0.95 ms
Throughput : 17.28 ± 0.28 tokens/s


# benchmark MiniCPM-V-4_5-int8_ov
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python benchmark_vlm.py \
-m /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int8_ov  \
-i /root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
-p "图中有什么?" \
-n 3 \
-d GPU:1 # GPU:0(iGPU), GPU:1(Arc770)

## MiniCPM-V-4_5-int8_ov iGPU 性能 (显存占用9.1G)
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 15346.00 ms
Generate time: 10151.71 ± 8.49 ms
Tokenization time: 21.15 ± 0.14 ms
Detokenization time: 0.40 ± 0.06 ms
Embeddings preparation time: 24.97 ± 0.00 ms
TTFT: 7981.66 ± 3.46 ms
TPOT: 114.19 ± 1.53 ms
Throughput : 8.76 ± 0.12 tokens/s

## MiniCPM-V-4_5-int8_ov Arc770 性能 (显存占用9.8G) 
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 10262.00 ms
Generate time: 1351.68 ± 6.21 ms
Tokenization time: 22.88 ± 1.11 ms
Detokenization time: 1.10 ± 0.04 ms
Embeddings preparation time: 25.35 ± 0.00 ms
TTFT: 673.43 ± 3.86 ms
TPOT: 35.63 ± 2.19 ms
Throughput : 28.07 ± 1.73 tokens/s


# benchmark MiniCPM-V-4_5-int4_ov
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python benchmark_vlm.py \
-m /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int4_ov  \
-i /root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
-p "图中有什么?" \
-n 3 \
-d GPU:1 # GPU:0(iGPU), GPU:1(Arc770)

## MiniCPM-V-4_5-int4_ov iGPU 性能 (显存占用6G) 
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 12301.00 ms
Generate time: 8205.62 ± 5.66 ms
Tokenization time: 21.15 ± 0.15 ms
Detokenization time: 0.27 ± 0.01 ms
Embeddings preparation time: 25.46 ± 0.00 ms
TTFT: 6885.49 ± 6.00 ms
TPOT: 69.46 ± 0.76 ms
Throughput : 14.40 ± 0.16 tokens/s

## MiniCPM-V-4_5-int4_ov Arc770 性能 (显存占用6.4G)  
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 8659.00 ms
Generate time: 1122.64 ± 6.23 ms
Tokenization time: 23.32 ± 0.98 ms
Detokenization time: 0.57 ± 0.04 ms
Embeddings preparation time: 25.35 ± 0.00 ms
TTFT: 693.66 ± 2.74 ms
TPOT: 22.54 ± 4.78 ms
Throughput : 44.36 ± 9.40 tokens/s


```
