from textblob import TextBlob

# 文本情感分析示例
text = "TextBlob is a good library!"
# text = "TextBlob is a great library!"

blob = TextBlob(text)

# 返回浮点数，表示文本情感的极性。-1 表示最负面的情感，1 表示最正面的情感
sentiment = blob.sentiment.polarity
# 输出：0.875
print("情感分析结果：", sentiment)

# 返回元组，第一个值是情感极性（与 blob.sentiment.polarity 相同），第二个值是情感主观性。情感主观性是一个介于 0 和 1 之间的浮点数，其中 0 表示最客观的情感，1 表示最主观的情感。
sentiment = blob.sentiment
# 输出结果：情感分析结果： Sentiment(polarity=0.875, subjectivity=0.6000000000000001)
print("情感分析结果：", sentiment)


