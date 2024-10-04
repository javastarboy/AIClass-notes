from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string

# 文本预处理
text = "Gensim is a Python library for topic modeling, document indexing, and similarity retrieval with large corpora."
preprocessed_text = preprocess_string(text)

# 创建语料库
dictionary = corpora.Dictionary([preprocessed_text])
corpus = [dictionary.doc2bow(preprocessed_text)]

# 训练LDA主题模型
lda_model = LdaModel(corpus, num_topics=1, id2word=dictionary)
print("LDA主题模型结果：", lda_model.print_topics())