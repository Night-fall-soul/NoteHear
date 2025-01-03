import os
from openai import OpenAI


client = OpenAI (
    api_key="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",
)


model = "gpt-4o-mini"
messages = [
    {"role": "system", "content": "Tu es un redacteur professionnel des texts"},
    {"role": "user", "content": "Say this is a test!"}
    ]
temperature = 0.3
max_tokens = 500


completion = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens,
)
print(completion.choices[0].message.content, end="")




