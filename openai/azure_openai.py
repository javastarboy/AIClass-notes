import os
from openai import AzureOpenAI, azure_ad_token

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

azure_api_key = os.getenv('AZURE_API_KEY')
azure_base_url = os.getenv('AZURE_BASE_URL')
azure_api_version = os.getenv('AZURE_API_VERSION')

client = AzureOpenAI(
  api_key=azure_api_key,
  api_version=azure_api_version,
  azure_endpoint=azure_base_url
)

response = client.chat.completions.create(
    model="gpt35",
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)