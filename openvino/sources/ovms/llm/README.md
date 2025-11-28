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
# 吞吐量模式 批量处理任务
--throughput_model throughput
# 时延模式	实时应用、对话系统
--throughput_model low_latency	
# 平衡模式	通用场景
--throughput_model balanced	

# 查看支持的参数 
sudo docker run -it --rm openvino/model_server:2025.3-gpu --help

# start
models_path=/data/intel-workspace/intelai-platform-experiments/openvino/sources/genai/visual_language_chat/models
sudo docker run -it --rm \
--user root \
--device /dev/dri/renderD129:/dev/dri/renderD129 \
-p 8000:8000 \
-v ${models_path}:/models:rw openvino/model_server:2025.3-gpu \
--source_model MiniCPM-V-4_5-int8_ov \
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
curl http://localhost:8000/v3/chat/completions  \
-H "Content-Type: application/json" \
-d @${root_path}/sample/request_minicpm-v-4-5.json | jq -r '.choices[0].message.content'

```



# Benchmarking text generation with high concurrency
```shell
sudo docker exec -it intelai-platform-experiments_openvino /bin/bash
source /opt/benchmark-serving_venv/bin/activate  

# 登陆huggingface
huggingface-cli login


python /opt/vllm/benchmarks/benchmark_serving.py \
--backend openai-chat \
--dataset-name hf \
--dataset-path lmarena-ai/vision-arena-bench-v0.1 \
--hf-split train \
--host 172.17.0.1 \
--port 8000 \
--model MiniCPM-V-4_5-int8_ov \
--tokenizer /root/openvino/sources/genai/visual_language_chat/models/MiniCPM-V-4_5-int8_ov \
--endpoint /v3/chat/completions \
--max-concurrency 1 \
--num-prompts 100 \
--trust-remote-code




Model MiniCPM-V-4_5-int8_ov
Maximum request concurrency: 1
============ Serving Benchmark Result ============
Successful requests:                     100       
Benchmark duration (s):                  465.08    
Total input tokens:                      16589     
Total generated tokens:                  0         
Request throughput (req/s):              0.22      
Output token throughput (tok/s):         0.00      
Total Token throughput (tok/s):          35.67     
---------------Time to First Token----------------
Mean TTFT (ms):                          629.12    
Median TTFT (ms):                        597.71    
P99 TTFT (ms):                           1233.51   
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          0.00      
Median TPOT (ms):                        0.00      
P99 TPOT (ms):                           0.00      
---------------Inter-token Latency----------------
Mean ITL (ms):                           37.82     
Median ITL (ms):                         36.37     
P99 ITL (ms):                            108.71    
==================================================



Model MiniCPM-V-4_5-int4_ov
Maximum request concurrency: 1
============ Serving Benchmark Result ============
Successful requests:                     100       
Benchmark duration (s):                  315.35    
Total input tokens:                      16589     
Total generated tokens:                  0         
Request throughput (req/s):              0.32      
Output token throughput (tok/s):         0.00      
Total Token throughput (tok/s):          52.60     
---------------Time to First Token----------------
Mean TTFT (ms):                          601.36    
Median TTFT (ms):                        576.95    
P99 TTFT (ms):                           1200.61   
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          0.00      
Median TPOT (ms):                        0.00      
P99 TPOT (ms):                           0.00      
---------------Inter-token Latency----------------
Mean ITL (ms):                           23.02     
Median ITL (ms):                         22.01     
P99 ITL (ms):                            65.60     
==================================================





```