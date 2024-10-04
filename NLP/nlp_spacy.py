import spacy

# 下载spacy en_core_web_sm 模型（仅首次使用需要）
spacy.cli.download("en_core_web_sm")

# 加载英文模型
nlp = spacy.load("en_core_web_sm")


text = "Apple is looking at buying U.K. startup for $1 billion"
doc = nlp(text)

# 命名实体识别示例
print("命名实体识别结果：")
for ent in doc.ents:
    print(ent.text, ent.label_)  # 输出：Apple ORG, U.K. GPE, $1 billion MONEY

print("\n===============================\n")

# 分词、词性标注示例
print("分词和词性标注结果：")
for token in doc:
    print(token.text, token.pos_)