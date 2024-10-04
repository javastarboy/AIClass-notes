from transformers import pipeline
from transformers.tools.evaluate_agent import classifier

# 加载情感分析模型
generator = pipeline("text-generation")

# 文本生成示例
text = "In the beginning"
result = generator(text, max_length=50)
print("文本生成结果：", result[0]["generated_text"])

# 文本情感分析示例
text = "Transformers is an exciting library for NLP tasks."
result = classifier(text)
print("情感分析结果：", result)