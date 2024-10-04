from langchain_community.document_loaders import PyMuPDFLoader


############################# 1、文档加载器 Document Loaders #############################

# pip install fitz pymupdf
loader = PyMuPDFLoader("AI大模型全栈通识课介绍.pdf")
pages = loader.load_and_split()

print(pages[0].page_content, "\n\n")

############################# 2、文档处理器 TextSplitter #############################
# pip install --upgrade langchain-text-splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 初始化RecursiveCharacterTextSplitter文本分隔器
# 设置分隔器的参数，用于控制文本分割的行为
text_splitter = RecursiveCharacterTextSplitter(
    # 每个文本块的最大大小为200个字符
    chunk_size=200,
    # 文本块之间的重叠大小为100个字符，确保上下文的连贯性
    chunk_overlap=100,
    # 使用len函数计算文本长度
    length_function=len,
    # 在每个文本块的开始位置添加索引，便于后续处理时定位信息源
    add_start_index=True,
)

paragraphs = text_splitter.create_documents([pages[0].page_content])
for para in paragraphs:
    print(para.page_content)
    print('-------')



############################# 3、向量数据库与向量检索 #############################
# 见 langchain_004