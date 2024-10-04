from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyMuPDFLoader
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# langchain 向量数据库与向量检索

# 加载文档
loader = PyMuPDFLoader("AI大模型全栈通识课介绍.pdf")
pages = loader.load_and_split()

# 文档切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True,
)

# 从pages列表的前4个元素中提取page_content内容，并将其作为文档内容源
texts = text_splitter.create_documents(
    [page.page_content for page in pages[:4]]
)

# 灌库
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key, base_url=base_url)
# 从文本和嵌入式向量创建FAISS数据库
db = FAISS.from_documents(texts, embeddings)

# 检索 top-3 结果
retriever = db.as_retriever(search_kwargs={"k": 3})

docs = retriever.invoke("AI大模型全栈通识课适宜人群")

for doc in docs:
    print(doc.page_content)
    print("----")