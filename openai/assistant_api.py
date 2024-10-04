from openai import OpenAI
import os
from typing_extensions import override
from openai import AssistantEventHandler
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

# 初始化 OpenAI 服务
client = OpenAI(api_key=api_key, base_url=base_url)


def show_json(obj):
    """把任意对象用排版美观的 JSON 格式打印出来"""
    print(json.dumps(
        json.loads(obj.model_dump_json()),
        indent=4,
        ensure_ascii=False
    ))


# 1、创建助手

assistant = client.beta.assistants.create(
    name="AI大模型全栈通识课",
    instructions="你是AGI舰长，AI大模型全栈课堂的智能助理。你负责回答与本课堂的一些常见问题，并回答问题。",
    model="gpt-4o",
)

print(assistant.id)

# 2、创建 thread

# 可以根据需要，自定义 `metadata`，比如创建 thread 时，把 thread 归属的用户信息存入。
thread = client.beta.threads.create(
    metadata={"fullname": "AGI舰长", "username": "LHYYH0001"}
)
show_json(thread)

# Thread ID 如果保存下来，是可以在下次运行时继续对话的。
# 从 thread ID 获取 thread 对象的代码：
thread = client.beta.threads.retrieve(thread.id)
show_json(thread)

# 给 Threads 添加 Messages
# 这里的 messages 结构要复杂一些：
#   1. 不仅有文本，还可以有图片和文件
#   2. 也有 `metadata`
message = client.beta.threads.messages.create(
    thread_id=thread.id,  # message 必须归属于一个 thread
    role="user",  # 取值是 user 或者 assistant。但 assistant 消息会被自动加入，我们一般不需要自己构造
    content="AI全栈通识课适宜人群",
)
show_json(message)

# 3、Run

# 也可以从 Playground 中拷贝
assistant_id = assistant.id

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant_id,
)
if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    show_json(messages)
else:
    print(run.status)


# 流式运行，创建回调函数
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        """响应输出创建事件"""
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """响应输出生成的流片段"""
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

# 3、流式传输响应方式 Run
# with client.beta.threads.runs.stream(
#         thread_id=thread.id,
#         assistant_id=assistant_id,
#         event_handler=EventHandler(),
# ) as stream:
#     stream.until_done()
