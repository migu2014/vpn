# -*- coding: utf-8 -*-
import requests, re, os, time
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename='/root/clash.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


save_dir = "/usr/local/nginx/html/clash"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

# 获取页面内容
def html(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        logging.error('response ' + url + ' status = ' + str(response.status_code))
        raise RuntimeError('响应码错误 ' + response.status_code)

# 保存yaml文件
def yaml(link, filename):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers, stream=True)
    if response.status_code == 200:
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)
        with open(file_path, "wb") as f:
            comment = datetime.now().strftime("# %Y-%m-%d %H:%M:%S \n")
            f.write(comment.encode("utf-8"))
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # 避免空块
                    f.write(chunk)
        print(f"文件已下载：{filename}")
    else:
        print("请求失败，状态码:", response.status_code)
        logging.error('response ' + link + ' status = ' + str(response.status_code))

def mibei77():
    try:
        content = html('https://www.mibei77.com/category/jiedian?nofilter=true')
        soup = BeautifulSoup(content, "html.parser")
        a = soup.select('.item-heading a')[0]
        href = a["href"]
        content = html(href)
        soup = BeautifulSoup(content, "html.parser")
        for p in soup.select('.wp-posts-content p'):
            text = p.get_text(strip=True)
            if text.startswith('https://') and text.endswith('.yaml'):
                yaml(text, 'mibei77.yaml')
                break
    except Exception as e:
        logging.exception(f"exception occurs when request mibei77,traceback is:\n{e}")

def _85la():
    try:
        content = html('https://www.85la.com/internet-access/free-network-nodes')
        soup = BeautifulSoup(content, "html.parser")
        a = soup.select('.catleader a')[0]
        href = a["href"]
        content = html(href)
        soup = BeautifulSoup(content, "html.parser")
        for h3 in soup.find_all('h3'):
            if h3.get_text(strip=True).find('Clash.Mihomo 订阅地址') > -1:
                p = h3.find_next_sibling()
                a = p.find('a', recursive=False)
                yaml(a['href'], '85la.yaml')
                break
    except Exception as e:
        logging.exception(f"exception occurs when request 85la,traceback is:\n{e}")

def clashnode(n):
    url = 'https://node.clashnode.cc/uploads/' + time.strftime("%Y/%m/" + n + "-%Y%m%d", time.localtime()) + '.yaml'
    yaml(url, "0-clashnode.yaml")

def datiya():
    url = 'https://free.datiya.com/uploads/' + time.strftime("%Y%m%d", time.localtime()) + '-clash.yaml'
    yaml(url, 'datiya.yaml')


mibei77()
clashnode("0")