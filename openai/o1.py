import os

from openai import OpenAI

"""
升级 openai 包版本至少到 openai-1.50.0
pip install --upgrade openai
"""
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

model = "o1-mini"
client = OpenAI(api_key=api_key, base_url=base_url)
chat_completion = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "user", "content": "9.11 与 9.9 哪个大"}
    ],
)
print("==========================================================")
print("o1-mini回答：")
print(chat_completion.choices[0].message.content)
print("==========================================================\n\n")


model = "gpt-4o-mini"
chat_completion = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "user", "content": "9.11 与 9.9 哪个大"}
    ],
)
print("==========================================================")
print("gpt-4o-mini回答：")
print(chat_completion.choices[0].message.content)
print("==========================================================")
