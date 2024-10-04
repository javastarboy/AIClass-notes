import re


def main(text: str) -> dict:
    """
    中文字数统计，用于大模型 agent 中字数的控制
    1. 数字或年份（例如：2024, 89, 29）应计为一个字。无论数字的长度如何，每个独立的数字都算作一个字。
    2. 英语单词被视为一个单独的字。我们要确保单个单词连续的英文字母作为一个字计算。
    3. 标点符号（如逗号、句号等）也每个算作一个字。

    例子：在2024年的春天，小明和小华去了New York观光。他们在那里停留了5天，体验非常棒！
        纯汉字是 28 个
        数字是 2 个：分别为 2024 和 5
        标点符号是 4 个：，。!
        英文单词 2 个：New York
    :param text:
    :return:
    """
    # 匹配中文字符
    chinese_characters = re.findall(r'[\u4e00-\u9fff]', text)
    # 匹配数字（连续数字作为一个单位）
    numbers = re.findall(r'\d+', text)
    # 匹配英文单词
    english_words = re.findall(r'[A-Za-z]+', text)
    # english_words = re.findall(r'[A-Za-z]+(?:-[A-Za-z0-9]+)*', text)

    # 匹配标点符号
    punctuation = re.findall(r'[，。？！；：“”、（）《》—-]', text)

    # 计算总字数
    total_count = len(chinese_characters) + len(numbers) + len(english_words) + len(punctuation)

    word_count = str(total_count)

    return {
        "result": word_count,
    }


print(main("在2024年的春天，小明和小华去了New York观光。他们在那里停留了5天，体验非常棒！"))