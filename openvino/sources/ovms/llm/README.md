# Doc
```shell

https://docs.openvino.ai/2025/model-server/ovms_docs_llm_quickstart.html

# Serve VLM on OVMS
https://docs.openvino.ai/2025/model-server/ovms_demos_continuous_batching_vlm.html


# VLLM Benchmarking
https://docs.openvino.ai/2025/model-server/ovms_demos_continuous_batching_vlm.html


```

# Deploy the Model
```shell

# 查看支持的参数 
sudo docker run -it --rm openvino/model_server:2025.3-gpu --help

# start
models_path=/data/intel-workspace/intelai-platform-experiments/openvino/sources/genai/visual_language_chat/models
sudo docker run -it --rm \
--user root \
--device /dev/dri/renderD129:/dev/dri/renderD129 \
-p 8000:8000 \
-v ${models_path}:/models:rw openvino/model_server:2025.3-gpu \
--source_model MiniCPM-V-4_5-int4_ov \
--pipeline_type VLM \
--model_repository_path models \
--task text_generation \
--pipeline_type VLM \
--max_num_batched_tokens 99999 \
--enable_tool_guided_generation true \
--rest_port 8000 \
--target_device GPU \
--cache_size 2



```

# Check Model Readiness
```shell

curl http://localhost:8000/v1/config

```

# Run Generation
```shell


# 1. 生成 base64 字符串（不带 data URL 前缀先）
root_path=/data/intel-workspace/intelai-platform-experiments/openvino/sources/ovms/llm
BASE64_IMG=$(base64 -w 0 "${root_path}/sample/6ff1643f00a6b1a63f343a08300d557f.jpg")

# 2. 构造 JSON 请求体并写入临时文件
cat > ${root_path}/sample/request_minicpm-v-4-5.json <<EOF
{
  "model": "MiniCPM-V-4_5-int4_ov",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "请描述这张图片, 回答50字以内"},
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,${BASE64_IMG}"
          }
        }
      ]
    }
  ],
  "temperature": 0.0,
  "chat_template_kwargs": {
    "enable_thinking": false
  },
  "stop_token_ids": [1, 73440]
}
EOF

# 3. 用 curl 从文件读取 body
root_path=/data/intel-workspace/intelai-platform-experiments/openvino/sources/ovms/llm
curl http://localhost:8000/v3/chat/completions  \
-H "Content-Type: application/json" \
-d @${root_path}/sample/request_minicpm-v-4-5.json | jq -r '.choices[0].message.content'

```


# Download model
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/benchmark-serving_venv/bin/activate  

pip install modelscope
modelscope download --dataset lmarena-ai/vision-arena-bench-v0.1 --local_dir /root/openvino/sources/ovms/llm/datasets/vision-arena-bench-v0.1

```


# Benchmarking text generation with high concurrency
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/benchmark-serving_venv/bin/activate  

# copy benchmark_serving
mv /opt/vllm/benchmarks/benchmark_serving.py /opt/vllm/benchmarks/benchmark_serving.py.bak
cp /root/openvino/sources/ovms/llm/benchmark_serving.py /opt/vllm/benchmarks/

# run
python /opt/vllm/benchmarks/benchmark_serving.py \
--backend openai-chat \
--dataset-name hf \
--dataset-path /root/openvino/sources/ovms/llm/datasets/vision-arena-bench-v0.1 \
--hf-split train \
--host 172.17.0.1 \
--port 8000 \
--model MiniCPM-V-4_5-int4_ov \
--tokenizer /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int4_ov \
--endpoint /v3/chat/completions \
--max-concurrency 1 \
--num-prompts 100 \
--trust-remote-code



# result
Model MiniCPM-V-4_5-int4_ov
Maximum request concurrency: 1
GPU Memory: 6.8G
Execution time: 3.23s/it]
============ Serving Benchmark Result ============
Successful requests:                     100       
Benchmark duration (s):                  317.55    
Total input tokens:                      16589     
Total generated tokens:                  11647     
Request throughput (req/s):              0.31      
Output token throughput (tok/s):         36.68     
Total Token throughput (tok/s):          88.92     
---------------Time to First Token----------------
Mean TTFT (ms):                          621.04    
Median TTFT (ms):                        582.43    
P99 TTFT (ms):                           1207.48   
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          22.12     
Median TPOT (ms):                        22.00     
P99 TPOT (ms):                           23.88     
---------------Inter-token Latency----------------
Mean ITL (ms):                           23.03     
Median ITL (ms):                         22.03     
P99 ITL (ms):                            65.56     



Model MiniCPM-V-4_5-int8_ov
Maximum request concurrency: 1
GPU Memory: 10.0G
Execution time: 4.8s/it]
============ Serving Benchmark Result ============
Successful requests:                     100       
Benchmark duration (s):                  464.94    
Total input tokens:                      16589     
Total generated tokens:                  11333     
Request throughput (req/s):              0.22      
Output token throughput (tok/s):         24.38     
Total Token throughput (tok/s):          60.06     
---------------Time to First Token----------------
Mean TTFT (ms):                          628.89    
Median TTFT (ms):                        595.48    
P99 TTFT (ms):                           1243.07   
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          35.07     
Median TPOT (ms):                        35.68     
P99 TPOT (ms):                           37.38     
---------------Inter-token Latency----------------
Mean ITL (ms):                           37.80     
Median ITL (ms):                         36.36     
P99 ITL (ms):                            108.88    
==================================================


Model MiniCPM-V-4_5-int8_ov
Maximum request concurrency: 1
GPU Memory: 10.0G
Execution time: 4.52s/it]
============ Serving Benchmark Result ============
Successful requests:                     100       
Benchmark duration (s):                  452.31    
Total input tokens:                      16589     
Total generated tokens:                  11338     
Request throughput (req/s):              0.22      
Output token throughput (tok/s):         25.07     
Total Token throughput (tok/s):          61.74     
---------------Time to First Token----------------
Mean TTFT (ms):                          4975.20   
Median TTFT (ms):                        5416.15   
P99 TTFT (ms):                           7753.81   
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          35.37     
Median TPOT (ms):                        35.69     
P99 TPOT (ms):                           37.63     
---------------Inter-token Latency----------------
Mean ITL (ms):                           37.80     
Median ITL (ms):                         36.38     
P99 ITL (ms):                            108.59    
==================================================



```