import json
import os

import requests

# pip install --upgrade openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

MODEL = "gpt-4o"

ROLE_USER = "user"
ROLE_SYSTEM = "system"
ROLE_ASSISTANT = "assistant"

messages = []
# 设置请求头
headers = {
    "Content-Type": "application/json",
    "Accept-Charset": "utf-8",
    "Authorization": "Bearer " + api_key,
    "check": "1"
}


def completion(prompt):
    """流式交互示例"""
    field = {
        "model": MODEL,
        "messages": prompt,
        "stream": True
    }
    # 发送 HTTP POST 请求
    response = requests.post(base_url, headers=headers, data=json.dumps(field), stream=True)
    # print(response.text)
    return response.content.decode("utf-8")


def dealMsg(role, msg):
    messages.append({"role": role, "content": msg})
    return messages


# 运行业务代码
print("[AI|:]" + completion(dealMsg(ROLE_USER, input("You|: "))))
