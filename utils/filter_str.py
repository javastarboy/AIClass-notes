def main(text: str) -> dict:
    # 将 \\n 转换为 换行符
    s = text.replace("\\n", "\n")

    # 去掉字符串开头和结尾的双引号
    if s.startswith('\"'):
        s = s[1:]
    if s.endswith('\"'):
        s = s[:-1]

    return {
        "result": s,
    }
