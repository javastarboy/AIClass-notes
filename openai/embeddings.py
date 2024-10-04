import os

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

client = OpenAI(api_key=api_key, base_url=base_url)

'''
text-embedding-3-small 
text-embedding-3-large
text-embedding-3-ada-002
'''
response = client.embeddings.create(
  model="text-embedding-3-small",
  input="我是大聪明...",
  encoding_format="float"
)

print(response.data[0])
