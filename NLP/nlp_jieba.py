import jieba

text = "我喜欢自然语言处理技术！"
seg_list = jieba.cut(text, cut_all=False)
print("精确模式分词结果：", "/".join(seg_list))

#添加自定义词典
jieba.add_word("自然语言处理")
seg_list_custom = jieba.cut(text, cut_all=False)
print("添加自定义词典后的分词结果：", "/".join(seg_list_custom))