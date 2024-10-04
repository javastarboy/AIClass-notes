# 初始化
import os

from openai import OpenAI
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

client = OpenAI(api_key=api_key, base_url=base_url)

def print_json(data):
    """
    打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
    否则，直接打印该值。
    """
    if hasattr(data, 'model_dump_json'):
        data = json.loads(data.model_dump_json())

    if isinstance(data, (list)):
        for item in data:
            print_json(item)
    elif isinstance(data, (dict)):
        print(json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ))
    else:
        print(data)


def get_completion(messages, model="gpt-4o"):
    """
    定义 sum 函数 tools
    :param messages: 上下文
    :param model: 模型
    :return:
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        tools=[{  # 用 JSON 描述函数。可以定义多个。由大模型决定调用谁。也可能都不调用
            "type": "function",
            "function": {
                "name": "sum",
                "description": "加法器，计算一组数的和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                }
            }
        }],
    )
    return response.choices[0].message


# 测试用例（四个场景挨个试试）
# prompt = "Tell me the sum of 1, 2, 3, 4, 5, 6, 7, 8, 9, 10."
prompt = "桌上有 2 个苹果，四个桃子和 3 本书，还有 3 个番茄，以及三个傻瓜，一共有几个水果？"
# prompt = "1+2+3...+99+100"
# prompt = "1024 乘以 1024 是多少？"   # Tools 里没有定义乘法，会怎样？
# prompt = "太阳从哪边升起？"           # 不需要算加法，会怎样？

messages = [
    {"role": "system", "content": "你是一个数学家"},
    {"role": "user", "content": prompt}
]
response = get_completion(messages)

# 把大模型的回复加入到对话历史中。必须有
messages.append(response)

# 如果返回的是函数调用结果，则打印出来
if response.tool_calls is not None:
    # 是否要调用 sum
    tool_call = response.tool_calls[0]
    if tool_call.function.name == "sum":
        # 调用 sum
        args = json.loads(tool_call.function.arguments)
        result = sum(args["numbers"])

        # 把函数调用结果加入到对话历史中
        messages.append(
            {
                "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
                "role": "tool",
                "name": "sum",
                "content": str(result)  # 数值 result 必须转成字符串
            }
        )

        # 再次调用大模型
        response = get_completion(messages)
        messages.append(response)
        print("=====最终 GPT 回复=====")
        print(response.content)

print("=====对话历史=====")
print_json(messages)