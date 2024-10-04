# coding: utf-8
from PIL import Image, ImageFont
import os

from handright import Template, handwrite

fontName = "Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf"
# fontName = "/System/Library/Fonts/PingFang.ttc"

"""
生成随机风格的签名
"""
text = """AGI舰长"""

template = Template(
    background=Image.new(mode="1", size=(600, 800), color=1),
    font=ImageFont.truetype(fontName, size=100),
    line_spacing=150,
    fill=0,  # 字体“颜色”
    left_margin=100,
    top_margin=100,
    right_margin=100,
    bottom_margin=100,
    word_spacing=15,
    line_spacing_sigma=6,  # 行间距随机扰动
    font_size_sigma=20,  # 字体大小随机扰动
    word_spacing_sigma=3,  # 字间距随机扰动
    start_chars="“（[<",  # 特定字符提前换行，防止出现在行尾
    end_chars="，。",  # 防止特定字符因排版算法的自动换行而出现在行首
    perturb_x_sigma=4,  # 笔画横向偏移随机扰动
    perturb_y_sigma=4,  # 笔画纵向偏移随机扰动
    perturb_theta_sigma=0.05,  # 笔画旋转偏移随机扰动
)


# 获取当前工作目录
current_dir = os.getcwd()
images = handwrite(text, template)
for i, im in enumerate(images):
    assert isinstance(im, Image.Image)
    im.show()
    im.save(current_dir + "/{}.png".format(i))