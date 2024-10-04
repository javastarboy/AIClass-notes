import os

from openai import OpenAI

# pip install python-dotenv openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# OpenAI DALL-e3 图像模型接口
response = client.images.generate(
  model="dall-e-3",
  prompt="一只可爱的猫",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url)
