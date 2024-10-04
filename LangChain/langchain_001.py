import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain_openai import ChatOpenAI

"""
依赖安装
pip install --upgrade langchain
pip install --upgrade langchain-openai
pip install --upgrade langchain-community
"""

############################# 1、OpenAI Chat API 初体验 #############################
# 获取 api_key，请大家先将 .env.templet 文件重命名为 .env 后配置你的 url 以及 key 即可
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

llm = ChatOpenAI(model="gpt-4o",
                 temperature=0,
                 max_tokens=None,
                 timeout=None,
                 max_retries=2,
                 api_key=api_key,
                 base_url=base_url)
response = llm.invoke("你是谁")
# 我是一个由OpenAI开发的人工智能助手，旨在帮助回答问题、提供信息和协助完成各种任务。你可以问我任何问题，我会尽力提供有用的回答。有什么我可以帮你的吗？
print(response.content)


############################# 2、多轮对话 message #############################
from langchain.schema import (
    AIMessage,  # 等价于 OpenAI 接口中的 assistant role
    HumanMessage,  # 等价于 OpenAI 接口中的 user role
    SystemMessage  # 等价于 OpenAI 接口中的 system role
)

messages = [
    SystemMessage(content="你是「AI大模型全栈通识课」的课程助理。"),
    HumanMessage(content="我是学员，我叫AGI舰长。微信号：LHYYH0001"),
    AIMessage(content="欢迎！"),
    HumanMessage(content="我是谁")
]
ret = llm.invoke(messages)
print(ret.content)


############################# 3、国产模型通义千问 #############################
# 其它模型分装在 langchain_community 底包中
from langchain_community.chat_models import ChatTongyi

# LangChain 中不支持企业转发，需要使用通义千问官方的 key
TONGYI_KEY = os.getenv('TONGYI_KEY')
tongyi_chat = ChatTongyi(
    api_key=TONGYI_KEY
)

messages = [
    ("system", "你是「AI大模型全栈通识课」的课程助理。你叫AGI舰长。微信号：LHYYH0001"),
    ("human", "你是谁？"),
]
ai_msg = tongyi_chat.invoke(messages)
print(ai_msg.content)