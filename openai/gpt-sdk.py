import os

import openai
from openai import OpenAI

# pip install --upgrade openai
# api_key = '你的 api_key'
# base_url = '你的 base_url/v1'

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

client = OpenAI(api_key=api_key, base_url=base_url)
# print(client.models.list())

# model = 'o1-preview'
# model = 'o1-mini'
model = 'gpt-4o-mini'
completion = client.chat.completions.create(
  model=model,
  messages=[
    # {"role": "system", "content": "你是一名人工智能万能助手"},
    {"role": "user", "content": "9.11 与 9.9 哪个大"}
  ]
)

print(completion.choices[0].message.content)

