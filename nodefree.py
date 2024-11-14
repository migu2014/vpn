import os
import requests
from bs4 import BeautifulSoup

print('开始抓取nodefree网页内容...')
# 设置要抓取的网页URL
url = 'https://nodefree.org/'

# 设置请求头，伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
# 发起请求
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    a = soup.select_one('ul.post-loop > li.item > div.item-img > a.item-img-inner')
    if a:
        print(a.get('href'))  # 打印链接
        response = requests.get(a.get('href'), headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('div.document > div.section > p')
            os.chdir('/media/AiCard_01/hwf_download/mobile/document/vpn/')
            for item in items:
                if item.text.endswith('.yaml'):
                    yaml = item.text
                    os.system('rm -rf nodefree.yaml')
                    os.system('wget ' + yaml + ' -O nodefree.yaml')
                    break
            os.system('git add .')
            os.system('git commit -m \'m\'')
            os.system('git push origin main')
    else:
        print('未找到指定的元素')
else:
    print('请求失败，状态码:', response.status_code)