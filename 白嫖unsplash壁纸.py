import requests
import time
import re
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

def url(info, numbers):
    for i in range(1, numbers+1):
        url = 'https://unsplash.com/napi/search/photos?query=' + info +'&xp=&per_page=20&page=' + str(i)
        headers = {
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',

        }
        req = requests.get(url=url, headers=headers)
        key = r'"download":"https://unsplash.com/photos/(.*?)/download"'  # 下载图片的固定url
        c = re.findall(key, req.text, re.S)
        for id in c:
            time.sleep(2)
            download_url = 'https://unsplash.com/photos/'+id+'/download'
            try:
                urlretrieve(url=download_url, filename=id + '.jpg')
            except:
                print('something bad')
                continue

info = input('请输入你想要输入的类型：')
numbers = int(int(input('请输入你想下载的图片数量（请确保是10的倍数：')) / 10)
url(info=info, numbers=numbers)