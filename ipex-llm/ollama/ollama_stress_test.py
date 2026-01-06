import aiohttp
import asyncio
import time
import json
import subprocess
import shlex

async def send_request_non_streaming(session, prompt, i):
    """非流式请求，用于统计生成速度"""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "deepseek-r1:7b",
        "prompt": prompt,
        "stream": False
    }
    
    start_time = time.time()
    
    try:
        async with session.post(url, json=data) as response:
            result = await response.json()
            end_time = time.time()
            
            total_duration = end_time - start_time
            generated_tokens = result.get("eval_count", 0)
            response_text = result.get("response", "")
            
            print(f"非流式请求 {i}: 生成 {generated_tokens} tokens, 耗时 {total_duration:.2f}s")
            
            return {
                "total_duration": total_duration,
                "generated_tokens": generated_tokens,
                "response_text": response_text,
                "success": True,
                "start_time": start_time,
                "end_time": end_time
            }
            
    except Exception as e:
        print(f"非流式请求 {i} 失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

async def send_request_streaming(session, prompt, i, timeout=30):
    """流式请求，通过 Python 包装 shell 脚本实现，只等第一个非空 response"""
    start_time = time.time()
    
    try:
        # 构建 shell 脚本命令
        shell_script = f'''#!/bin/bash
start_time=$(date +%s%N)
line=$(curl -s http://localhost:11434/api/generate \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "deepseek-r1:7b",
    "prompt": "{prompt}",
    "stream": true
  }}' | grep -m1 '"response"' | head -n1)

if [ -n "$line" ]; then
  first_token_time=$(date +%s%N)
  ttft_ms=$(( (first_token_time - start_time) / 1000000 ))
  echo "TTFT: ${{ttft_ms}}"
  echo "RESPONSE: $line"
else
  echo "ERROR: no response received"
fi
'''
        
        # 使用 asyncio 执行 shell 脚本
        async with asyncio.timeout(timeout):
            # 创建临时 shell 脚本文件
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(shell_script)
                temp_script = f.name
            
            try:
                # 设置脚本可执行权限
                os.chmod(temp_script, 0o755)
                
                # 执行 shell 脚本
                process = await asyncio.create_subprocess_exec(
                    'bash', temp_script,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    output = stdout.decode('utf-8').strip()
                    
                    # 解析输出
                    lines = output.split('\n')
                    ttft_line = None
                    response_line = None
                    
                    for line in lines:
                        if line.startswith('TTFT:'):
                            ttft_line = line
                        elif line.startswith('RESPONSE:'):
                            response_line = line
                    
                    if ttft_line and response_line:
                        # 提取 TTFT 时间（毫秒转换为秒）
                        ttft_ms = int(ttft_line.split(':')[1].strip())
                        ttft_seconds = ttft_ms / 1000.0
                        
                        # 提取响应内容
                        response_content = response_line.split(':', 1)[1].strip()
                        
                        print(f"✅ 流式请求 {i}: 首Token在 {ttft_seconds:.3f}s 到达 → '{response_content[:50]}...'")
                        
                        return {
                            "first_token_time": ttft_seconds,
                            "first_token_content": response_content,
                            "success": True,
                            "has_first_token": True,
                            "total_duration": ttft_seconds,
                            "start_time": start_time,
                            "end_time": time.time()
                        }
                    else:
                        print(f"❌ 流式请求 {i}: 脚本输出格式错误")
                        return {
                            "success": False,
                            "error": "script output format error",
                            "has_first_token": False
                        }
                else:
                    stderr_output = stderr.decode('utf-8').strip()
                    print(f"❌ 流式请求 {i}: 脚本执行失败 - {stderr_output}")
                    return {
                        "success": False,
                        "error": f"script execution failed: {stderr_output}",
                        "has_first_token": False
                    }
                    
            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_script)
                except:
                    pass

    except asyncio.TimeoutError:
        print(f"❌ 流式请求 {i}: 超时")
        return {
            "success": False,
            "error": "timeout",
            "has_first_token": False
        }
    except Exception as e:
        print(f"❌ 流式请求 {i}: 执行出错 - {e}")
        return {
            "success": False,
            "error": str(e),
            "has_first_token": False
        }

async def run_comprehensive_test():
    """运行综合性能测试"""
    print("🤖 Ollama 综合性能测试")
    print("=" * 60)
    
    # 获取测试参数
    try:
        num_concurrent_requests = int(input("请输入并发请求数 (默认4): ") or "4")
        test_prompt = input("请输入测试提示词 (默认: 请用中文解释一下牛顿第一定律，要求800字。): ") or "请用中文解释一下牛顿第一定律，要求800字。"
    except ValueError:
        print("❌ 输入无效，使用默认值")
        num_concurrent_requests = 4
        test_prompt = "请用中文解释一下牛顿第一定律，要求800字。"

    print(f"\n测试配置:")
    print(f"并发数: {num_concurrent_requests}")
    print(f"提示词: '{test_prompt}'")
    
    # ==================== 第一阶段：非流式测试（生成速度） ====================
    print("\n" + "=" * 60)
    print("🚀 第一阶段: 非流式测试 (生成速度)")
    print("=" * 60)
    
    test_start_time = time.time()
    
    connector1 = aiohttp.TCPConnector(limit=num_concurrent_requests)
    async with aiohttp.ClientSession(connector=connector1) as session:
        tasks = [
            asyncio.create_task(send_request_non_streaming(session, test_prompt, i))
            for i in range(num_concurrent_requests)
        ]

        results = await asyncio.gather(*tasks)
        test_end_time = time.time()
        total_test_duration = test_end_time - test_start_time

        successful_results = [r for r in results if r.get("success")]
        
        if successful_results:
            individual_durations = [r["total_duration"] for r in successful_results]
            total_tokens = sum(r["generated_tokens"] for r in successful_results)
            avg_duration = sum(individual_durations) / len(successful_results)
            avg_tokens = total_tokens / len(successful_results)
            avg_speed_tokens_per_sec = total_tokens / total_test_duration

            print(f"\n📊 非流式测试结果 ({len(successful_results)} 个成功请求):")
            print("-" * 50)
            print(f"并发测试总耗时: {total_test_duration:.2f} 秒")
            print(f"总生成Token数: {total_tokens}")
            print(f"平均每个请求Token数: {avg_tokens:.1f}")
            print(f"平均每个请求耗时: {avg_duration:.2f} 秒")
            print(f"最快请求耗时: {min(individual_durations):.2f} 秒")
            print(f"最慢请求耗时: {max(individual_durations):.2f} 秒")
            print(f"🎯 系统平均生成速度: {avg_speed_tokens_per_sec:.2f} tokens/秒")
            print(f"系统吞吐量: {len(successful_results) / total_test_duration:.2f} 请求/秒")
            
            if successful_results[0]["response_text"]:
                sample = successful_results[0]["response_text"]
                print(f"\n📝 样本响应: '{sample[:100]}{'...' if len(sample) > 100 else ''}'")
        else:
            print("❌ 所有非流式请求都失败了！")
    
    await asyncio.sleep(1)
    
    # ==================== 第二阶段：流式测试（首Token耗时） ====================
    print("\n" + "=" * 60)
    print("⏱️  第二阶段: 流式测试 (首Token耗时)")
    print("=" * 60)
    
    test_start_time = time.time()
    
    connector2 = aiohttp.TCPConnector(limit=num_concurrent_requests)
    async with aiohttp.ClientSession(connector=connector2) as session:
        tasks = [
            asyncio.create_task(send_request_streaming(session, test_prompt, i, timeout=30))
            for i in range(num_concurrent_requests)
        ]

        results = await asyncio.gather(*tasks)
        test_end_time = time.time()
        total_test_duration = test_end_time - test_start_time

        successful_results = [r for r in results if r.get("success")]
        results_with_first_token = [r for r in successful_results if r.get("has_first_token")]

        print(f"\n📊 流式测试结果:")
        print("-" * 50)
        print(f"并发测试总耗时: {total_test_duration:.2f} 秒")
        print(f"总请求数: {len(results)}")
        print(f"成功请求: {len(successful_results)}")
        print(f"成功且有首Token: {len(results_with_first_token)}")
        
        if results_with_first_token:
            first_token_times = [r["first_token_time"] for r in results_with_first_token]
            first_token_contents = [r["first_token_content"] for r in results_with_first_token]
            avg_ttft = sum(first_token_times) / len(first_token_times)
            min_ttft = min(first_token_times)
            max_ttft = max(first_token_times)
            avg_speed = sum(r.get("generated_tokens", 0) for r in results_with_first_token) / total_test_duration

            print(f"\n⏰ 首Token耗时统计 (TTFT):")
            print(f"平均 TTFT: {avg_ttft:.3f} 秒")
            print(f"最快: {min_ttft:.3f} 秒")
            print(f"最慢: {max_ttft:.3f} 秒")
            print(f"样本数: {len(first_token_times)}")

            print(f"\n📝 首Token内容样本:")
            for idx, content in enumerate(first_token_contents[:3]):
                print(f"  {idx+1}. '{content}'")

            print(f"\n📈 附加信息:")
            print(f"平均生成速度（估算）: {avg_speed:.2f} tokens/秒")
        else:
            print("❌ 没有成功获取到首Token时间数据")
            # 诊断信息
            for i, res in enumerate(successful_results):
                print(f"  请求 {i}: 接收到数据={res.get('received_any_data', False)}")

    print("\n" + "=" * 60)
    print("✅ 综合测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(run_comprehensive_test())
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")