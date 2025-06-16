import requests
import time
import psutil

# Settings to test (edit as needed)
models = [
    "deepcoder-7b-preview",    # Example: try your model names
    "mistral-7b",
    "llama-3-8b"
]
quantizations = ["F16", "Q8"]  # Change as per your LM Studio support
thread_pools = [4, 8, 16]
prompts = ["hi", "summarize this: LM Studio is great!", "translate to Afrikaans: AI will change the world."]

API_URL = "http://127.0.0.1:1234/v1/chat/completions"
headers = {"Content-Type": "application/json"}

results = []

for model in models:
    for quant in quantizations:
        for threads in thread_pools:
            # (You must manually set the model, quantization, and thread count in LM Studio before running this batch OR automate via LM Studio config if supported)
            print(f"*** TESTING: {model}, {quant}, Threads={threads} ***")
            times = []
            for prompt in prompts:
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 50,
                    "temperature": 0.5,
                }
                cpu_start = psutil.cpu_percent(interval=0.1)
                mem_start = psutil.virtual_memory().percent
                t0 = time.time()
                try:
                    response = requests.post(API_URL, json=data, headers=headers, timeout=60)
                    response.raise_for_status()
                    duration = time.time() - t0
                    times.append(duration)
                    cpu_end = psutil.cpu_percent(interval=0.1)
                    mem_end = psutil.virtual_memory().percent
                    print(f"Prompt: {prompt} | Time: {duration:.2f}s | CPU: {cpu_end-mem_start:.1f}% | RAM: {mem_end-mem_start:.1f}%")
                except Exception as e:
                    print(f"Error with {model}/{quant}/Threads={threads}: {e}")
                    times.append(None)
            avg_time = sum([t for t in times if t]) / len([t for t in times if t])
            results.append({
                "model": model,
                "quantization": quant,
                "threads": threads,
                "avg_response_time_s": avg_time
            })

print("\n=== BENCHMARK SUMMARY ===")
for res in results:
    print(res)
