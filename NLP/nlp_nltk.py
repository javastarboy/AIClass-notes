import nltk
from nltk.tokenize import word_tokenize

# 下载NLTK数据（仅首次使用需要）
nltk.download('punkt')

# 分词示例
text = "This is a sentence."
tokens = nltk.word_tokenize(text)
# 输出：['This', 'is', 'a', 'sentence', '.']
print("分词示例", tokens)


# 下载 NLTK 数据（仅首次使用需要）
nltk.download('averaged_perceptron_tagger')
# 词性标注示例
tagged_tokens = nltk.pos_tag(tokens)
# 输出：[('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('sentence', 'NN'), ('.', '.')]
print("词性标注示例", tagged_tokens)

"""解释
'This' 的词性是 'DT'（determiner，限定词）
'is' 的词性是 'VBZ'（verb，singular present，现在时的单数形式）
'a' 的词性是 'DT'（determiner，限定词）
'sentence' 的词性是 'NN'（noun，singular or mass，名词，单数或集合名词）
'.' 的词性是 '.'（ punctuation mark，标点符号）

例如，
'This' 是一个限定词，用来限定后面的名词，表明它所指的对象。
'is' 是一个动词，在这里是第三人称单数形式，表示存在。
'a' 也是一个限定词，用来修饰后面的名词 'sentence'，表明它所指的对象。
'sentence' 是一个名词，表示一个句子。
'.' 是一个标点符号，表示句子的结束。

词性标注是自然语言处理中的一项基础工作，它有助于计算机理解和解释文本。
"""