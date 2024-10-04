"""
增加购买数量会触发接口调用

1、获取价格
https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t=1727135140816&body={
    "skuId": 7510812,
    "cat": "36720,36724,39110",
    "area": "9_639_38630_61684",
    "shopId": "1000119842",
    "venderId": 1000119842,
    "paramJson": "{
        "platform2": "1",
        "specialAttrStr": "p0pppppppppppppppppppppp",
        "skuMarkStr": "00"
    }",
    "num": 2,
    "bbTraffic": "",
    "canvasType": 1,
    "giftServiceIsSelected": ""
  }&x-api-eid-token=jdd03VSPVWIPW7QG57FVONBY62GN2RKQA46WGEZHNLMP6ZKQ2HDC36HRUHA5QORE5OUEW3KFKPNEY4AHZ2P7B2KXJZQQWQQAAAAMSEFDMJKIAAAAADIRFQ3ADYVKU5IX&loginType=3&scval=7510812&uuid=181111935.16812870885021179654703.1681287088.1727086385.1727135137.102

2、获取店铺名称seller
https://api.m.jd.com/?appid=item-v3&functionId=checkChat&client=pc&clientVersion=1.0.0&t=1727135141100&loginType=3&body={
  "source": "jd_pc_item",
  "key": "JDPC_baf0bd4ca77d4e09847b97504b8763cf",
  "pid": 7510812,
  "returnCharset": "utf-8"
}&uuid=181111935.16812870885021179654703.1681287088.1727086385.1727135137.102
"""


#####################方式一################################
import json
import requests

"""
    京东查询商品价格方法
    skus 京东sku集合
"""
def jd_price(skuList):
    # 京东查询商品价格链接
    url = 'https://api.m.jd.com/api?appid=item-v3&functionId=pctradesoa_getprice&body='
    # 组装请求报文
    skuStr = ''
    for sku in skuList:
        skuStr += sku + ','
    req = '{"skuIds": "' + skuStr + '", "source": "pc-item"}'
    # 请求头信息
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36 '
    }
    # 发送请求并处理返回信息
    request = requests.get(url=url + req, headers=headers)
    resultJson = json.loads(request.text)
    print(request.text)
    return request.text

# 商品sku集合
skus = {'7510812'}
price = jd_price(skus)
print(price)

#####################方式二################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

"""
安装驱动：
    pip install selenium
    pip install webdriver-manager
注意：需要确保下载的ChromeDriver版本与你的Chrome浏览器版本相匹配，并且将其路径正确指定在代码中。这样你就可以控制ChromeDriver的版本和更新，但需要手动管理这些文件。
"""
def get_jd_price_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    # 设置ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get(url)
        # 给予页面充分加载的时间
        time.sleep(8)
        # 定位价格信息
        price_element = driver.find_element(By.CSS_SELECTOR, '.p-price .price')
        price = price_element.text.strip()

        return price
    except Exception as e:
        print(f"发生错误: {e}")
        return None
    finally:
        driver.quit()

# 示例 URL
url = 'https://item.jd.com/7510812.html'
price = get_jd_price_with_selenium(url)
if price:
    print(f"京东价格: ￥{price}")
else:
    print("未能获取价格")



######################方式三################################

import requests
from bs4 import BeautifulSoup

def get_jd_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        # 京东的价格通常包含在 class 为 'p-price' 的 div 标签中
        price_tag = soup.find('span', class_='p-price')  # 查找包含价格的标签

        print(price_tag)

        price = price_tag.text.strip()  # 获取价格文本并去除多余空白字符

        return price
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except AttributeError:
        print("无法找到价格信息")
        return None


# 示例 URL
url = 'https://item.jd.com/7510812.html'
price = get_jd_price(url)
if price:
    print(f"京东价格: {price}")
else:
    print("未能获取价格")

