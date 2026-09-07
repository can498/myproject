import json
import urllib.request

API_KEY = "sk-ws-H.EHXXEHI.4mZl.MEQCIAKmRL4tyh9cQOuMyp0NNa0-I_nSaQpfTeH9CR5FQaQVAiBFEd2M0Pw9-pO-YuNT02_B6AHGDvlTtjU10mvp3-HTEw"
URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# 测试 1：最简单的请求（不带 response_format）
body = json.dumps({
    "model": "qwen-turbo",
    "messages": [{"role": "user", "content": "hello"}],
    "temperature": 0.1,
}).encode("utf-8")

req = urllib.request.Request(
    URL,
    data=body,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("✅ 连接成功！")
        print("模型返回：", data["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    print(f"❌ HTTP 错误：{e.code}")
    print(f"错误详情：{e.read().decode('utf-8')}")
except Exception as e:
    print(f"❌ 其他错误：{e}")