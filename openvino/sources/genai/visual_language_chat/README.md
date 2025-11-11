# Doc
```shell

https://github.com/openvinotoolkit/openvino.genai/tree/master/samples/python/genai/visual_language_chat

```


# Download model
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/visual-language-chat_venv/bin/activate  

pip install modelscope
modelscope download --model OpenBMB/MiniCPM-V-4_5 --local_dir /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5
modelscope download --model OpenBMB/MiniCPM-V-4_5-int4 --local_dir /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int4
modelscope download --model OpenBMB/MiniCPM-V-2_6 --local_dir /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-2_6
modelscope download --model OpenBMB/MiniCPM-V-2_6-int4 --local_dir /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-2_6-int4


```

# Run the export with Optimum CLI
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/visual-language-chat_venv/bin/activate  

# export MiniCPM-V-2_6
optimum-cli export openvino \
--model /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-2_6 \
--task image-text-to-text \
--trust-remote-code \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-2_6_IR

# export MiniCPM-V-4_5
optimum-cli export openvino \
--model /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5 \
--task image-text-to-text \
--trust-remote-code \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5_IR


```

# Run genai/visual_language_chat
```shell

# run MiniCPM-V-2_6_IR
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python visual_language_chat.py \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-2_6_IR/ \
/root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
GPU

# run MiniCPM-V-4_5_IR
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python visual_language_chat.py \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5_IR/ \
/root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
GPU

```

# Run benchmark
```shell
# benchmark MiniCPM-V-2_6_IR
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python benchmark_vlm.py \
-m /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-2_6_IR  \
-i /root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
-p "图中有什么?" \
-n 3 \
-d GPU


## CPU 性能
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 3799.00 ms
Generate time: 22453.30 ± 11.31 ms
Tokenization time: 1.56 ± 0.01 ms
Detokenization time: 0.22 ± 0.01 ms
Embeddings preparation time: 4.13 ± 0.00 ms
TTFT: 20124.31 ± 8.00 ms
TPOT: 122.56 ± 2.66 ms
Throughput : 8.16 ± 0.18 tokens/s

## GPU 性能 
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Load time: 15636.00 ms
Generate time: 9986.42 ± 10.20 ms
Tokenization time: 2.01 ± 0.04 ms
Detokenization time: 0.33 ± 0.01 ms
Embeddings preparation time: 5.92 ± 0.00 ms
TTFT: 7918.96 ± 13.56 ms
TPOT: 108.79 ± 1.61 ms
Throughput : 9.19 ± 0.14 tokens/s


# benchmark MiniCPM-V-4_5_IR
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python benchmark_vlm.py \
-m /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5_IR  \
-i /root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
-p "图中有什么?" \
-n 3 \
-d GPU

## GPU 性能
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 14650.00 ms
Generate time: 9960.58 ± 7.48 ms
Tokenization time: 20.99 ± 0.06 ms
Detokenization time: 0.38 ± 0.04 ms
Embeddings preparation time: 24.96 ± 0.00 ms
TTFT: 7740.11 ± 11.14 ms
TPOT: 116.84 ± 1.50 ms
Throughput : 8.56 ± 0.11 tokens/s

```
