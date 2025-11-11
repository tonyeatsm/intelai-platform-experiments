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
GPU:1

# run MiniCPM-V-4_5_IR
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python visual_language_chat.py \
/root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5_IR/ \
/root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
GPU:1

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
-d GPU:1 # GPU:0(iGPU), GPU:1(Arc770)

## iGPU 性能
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

## Arc770 性能 
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 10528.00 ms
Generate time: 1301.39 ± 4.18 ms
Tokenization time: 3.10 ± 0.33 ms
Detokenization time: 1.01 ± 0.03 ms
Embeddings preparation time: 5.77 ± 0.00 ms
TTFT: 676.50 ± 6.50 ms
TPOT: 32.82 ± 1.75 ms
Throughput : 30.47 ± 1.63 tokens/s

# benchmark MiniCPM-V-4_5_IR
cd /opt/install/openvino.genai-2025.3.0.0/samples/python/visual_language_chat
python benchmark_vlm.py \
-m /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5_IR  \
-i /root/openvino/sources/genai/visual_language_chat/6ff1643f00a6b1a63f343a08300d557f.jpg \
-p "图中有什么?" \
-n 3 \
-d GPU:1 # GPU:0(iGPU), GPU:1(Arc770)

## iGPU 性能
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

## Arc770 性能 
openvino runtime version: 2025.3.0-19807-44526285f24-releases/2025/3
Number of images:1, Prompt token size: 4
Output token size: 20
Load time: 16892.00 ms
Generate time: 1393.61 ± 10.45 ms
Tokenization time: 26.10 ± 0.37 ms
Detokenization time: 0.76 ± 0.08 ms
Embeddings preparation time: 29.16 ± 0.00 ms
TTFT: 719.50 ± 3.93 ms
TPOT: 35.43 ± 2.06 ms
Throughput : 28.23 ± 1.64 tokens/s

```
