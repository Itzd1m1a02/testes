from openai import OpenAI

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key="98584974c2a3471293f6f804f2a356e2",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "quala a capital do Brasil?"}]
)

print(response.choices[0].message.content)