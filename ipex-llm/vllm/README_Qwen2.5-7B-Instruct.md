
# Start the vLLM Service
```shell
sudo docker exec -it ipex-llm-serving-xpu_arc /bin/bash

curl "https://x.com"

# verify the device is successfully mapped into the container
export ONEAPI_DEVICE_SELECTOR="level_zero:0"
sycl-ls #--ignore-device-selectors

# Lock GPU Frequencies
sudo xpu-smi config -d 0 -t 0 --frequencyrange 2400,2400 

# Download model
pip install modelscope
modelscope download --model Qwen/Qwen2.5-7B-Instruct --local_dir /root/ipex-llm/models/vllm/Qwen2.

##############################################
# start ollama server
export USE_XETLA=OFF  # 禁用 intel的XeTLA矩阵计算库
export SYCL_CACHE_PERSISTENT=1 # 启用 持久化的SYCL编译缓存
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=2 # 允许命令直接提交到设备,减少 GPU 命令排队延迟 0-禁用 1-启用 2-完全启用
export FI_PROVIDER=shm # 设置 libfabric 的通信传输方式为 shm（共享内存）用于进程间通信（IPC）或跨节点通信
export TORCH_LLM_ALLREDUCE=0

export CCL_WORKER_COUNT=8  # 设置 CCL 内部工作线程数      # On BMG, set CCL_WORKER_COUNT=1; otherwise, internal-oneccl will not function properly
export CCL_ATL_TRANSPORT=ofi # 设置 CCL 的 ATL（Advanced Transport Layer） 使用 ofi（OpenFabrics Interfaces）作为传输层
export CCL_ZE_IPC_EXCHANGE=sockets # 设置 Ze（Level Zero）进程间通信（IPC）句柄交换机制 为 sockets
export CCL_ATL_SHM=1 # 启用 CCL 的 共享内存（SHM）加速机制
export CCL_SAME_STREAM=1 # 让 CCL 通信操作与计算操作使用 相同的 SYCL stream（流）。
export CCL_BLOCKING_WAIT=0 # 设置 CCL 通信操作为 非阻塞模式。
export CCL_DG2_USM=1  # 启用 DG2 上的 USM（Unified Shared Memory）支持。Xeon CPU 支持 P2P（Peer-to-Peer）内存访问，不需要 USM.
     

export LOAD_IN_LOW_BIT="fp8"
export IPEX_LLM_LOWBIT=$LOAD_IN_LOW_BIT        # Ensures low-bit info is used for MoE; otherwise, IPEX's default MoE will be used
export VLLM_USE_V1=0        # Used to select between V0 and V1 engine

source /opt/intel/1ccl-wks/setvars.sh

numactl -C 0-11 python -m ipex_llm.vllm.xpu.entrypoints.openai.api_server \
  --port 8000 \
  --model "/root/ipex-llm/models/vllm/Qwen2.5-7B-Instruct/" \
  --served-model-name "Qwen2.5-7B-Instruct" \
  --trust-remote-code \
  --gpu-memory-utilization "0.95" \
  --device xpu \
  --dtype float16 \
  --enforce-eager \
  --load-in-low-bit $LOAD_IN_LOW_BIT \
  --max-model-len "2000" \
  --max-num-batched-tokens "3000" \
  --max-num-seqs "256" \
  --tensor-parallel-size "1" \
  --pipeline-parallel-size "1" \
  --block-size 8 \
  --distributed-executor-backend ray \
  --disable-async-output-proc \
  --generation-config vllm

```

# Test the vLLM Service
```shell
sudo docker exec -it ipex-llm-serving-xpu_arc /bin/bash

curl http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-d '{
      "model": "Qwen2.5-7B-Instruct",
      "prompt": "请用中文解释一下牛顿第一定律，要求800字。",
      "max_tokens": 1000
    }'



``` 


# Benchmarking
```shell
sudo docker exec -it ipex-llm-serving-xpu_arc /bin/bash

export batch_size=16
export input_length=50
export output_length=800
python /llm/vllm/benchmarks/benchmark_serving.py \
--model "/root/ipex-llm/models/vllm/Qwen2.5-7B-Instruct/" \
--served-model-name "Qwen2.5-7B-Instruct" \
--dataset-name random \
--trust_remote_code \
--ignore-eos \
--num_prompt $batch_size \
--random-input-len=$input_length \
--random-output-len=$output_length


============ Serving Benchmark Result ============
Successful requests:                     1         
Benchmark duration (s):                  42.24     
Total input tokens:                      50        
Total generated tokens:                  800       
Request throughput (req/s):              0.02      
Output token throughput (tok/s):         18.94     
Total Token throughput (tok/s):          20.12     
---------------Time to First Token----------------
Mean TTFT (ms):                          86.57     
Median TTFT (ms):                        86.57     
P99 TTFT (ms):                           86.57     
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          52.76     
Median TPOT (ms):                        52.76     
P99 TPOT (ms):                           52.76     
---------------Inter-token Latency----------------
Mean ITL (ms):                           52.76     
Median ITL (ms):                         51.83     
P99 ITL (ms):                            67.89     
==================================================

============ Serving Benchmark Result ============
Successful requests:                     8         
Benchmark duration (s):                  44.98     
Total input tokens:                      400       
Total generated tokens:                  6400      
Request throughput (req/s):              0.18      
Output token throughput (tok/s):         142.29    
Total Token throughput (tok/s):          151.18    
---------------Time to First Token----------------
Mean TTFT (ms):                          341.74    
Median TTFT (ms):                        377.48    
P99 TTFT (ms):                           378.68    
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          55.86     
Median TPOT (ms):                        55.82     
P99 TPOT (ms):                           56.15     
---------------Inter-token Latency----------------
Mean ITL (ms):                           55.86     
Median ITL (ms):                         54.70     
P99 ITL (ms):                            70.50    
==================================================

============ Serving Benchmark Result ============
Successful requests:                     16        
Benchmark duration (s):                  47.04     
Total input tokens:                      800       
Total generated tokens:                  12800     
Request throughput (req/s):              0.34      
Output token throughput (tok/s):         272.08    
Total Token throughput (tok/s):          289.09    
---------------Time to First Token----------------
Mean TTFT (ms):                          521.73    
Median TTFT (ms):                        549.68    
P99 TTFT (ms):                           551.75    
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          58.22     
Median TPOT (ms):                        58.19     
P99 TPOT (ms):                           58.67     
---------------Inter-token Latency----------------
Mean ITL (ms):                           58.22     
Median ITL (ms):                         57.25     
P99 ITL (ms):                            74.35     
==================================================

```
