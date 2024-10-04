import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

############################# 1、PromptTemplate 模版 #############################

# 1.1 模版的原理
template = PromptTemplate.from_template("给我讲个关于{subject}的笑话")
print("===Template===")
print(template)
print("===Prompt===")
print(template.format(subject='小明'))

#  1.2 调用大模型
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')
# 定义 LLM
llm = ChatOpenAI(api_key=api_key,base_url=base_url)

# 通过 Prompt 调用 LLM
ret = llm.invoke(template.format(subject='小明'))
# 打印输出
print("===调用大模型效果===")
print(ret.content)



############################# 2、ChatPromptTemplate 用模板表示的对话上下文 #############################
template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "你是{product}的客服助手。你的名字叫{name}"),
        HumanMessagePromptTemplate.from_template("{query}"),
    ]
)

llm = ChatOpenAI()
prompt = template.format_messages(
    product="AI大模型全栈通识课",
    name="AGI舰长",
    query="你是谁"
)

print("\n\n =======对话上下文 prompt=======\n", prompt)
ret = llm.invoke(prompt)
print(ret.content)


############################# 3、MessagesPlaceholder 把多轮对话变成模板 #############################
# 3.1 模版设定
human_prompt = "将你的回答翻译成 {language}."
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder("history"), human_message_template]
)

# 3.2 模版转换
human_message = HumanMessage(content="Who is Elon Musk?")
ai_message = AIMessage(
    content="Elon Musk is a billionaire entrepreneur, inventor, and industrial designer"
)
messages = chat_prompt.format_prompt(
    # 对 "history" 和 "language" 赋值
    history=[human_message, ai_message], language="中文"
)
print('\n\n模版转换后的 prompt ===\n', messages.to_messages())

# 3.3 请求大模型
result = llm.invoke(messages)
print('大模型返回结果 =====\n', result.content)



############################# 3、从文件加载 Prompt 模板 #############################
template = PromptTemplate.from_file("本地文件.txt")
print("\n\n===Template===")
print(template)
print("===Prompt===")
print(template.format(topic='AI大模型全栈通识课-适宜人群'))
