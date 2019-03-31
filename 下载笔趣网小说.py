#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests, sys, time
from bs4 import BeautifulSoup

target = 'https://www.biqukan.com/1_1094/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
file = open('一念永恒.txt', 'w', encoding='utf-8')
numbers = float(1315)
index = float(0)

def dl(url):
    req = requests.get(url=url, headers=headers)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    soup = bf.find_all('div', class_='showtxt')
    try:
        text1 = soup[0].text.replace(' ', '\n').replace('\xa0' * 8, '\n')
        file.write(download_name + '\n\n')
        file.writelines(text1)
	#注意此处的try except标识，为了保证跳过Indexerror错误
    except IndexError:
        pass

req2 = requests.get(url=target, headers=headers)
html2 = req2.text
bf2 = BeautifulSoup(html2, 'lxml')
soup2 = bf2.find_all('div', class_='listmain')
bf3 = BeautifulSoup(str(soup2), 'lxml')
begin_flag = False

for child in bf3.dl.children:
    if child != '\n':
        if child.string == u'《一念永恒》正文卷':
            begin_flag = True
        if begin_flag == True and child.a != None and child.string != u"正文":
            if '《三寸人间》' not in child.string:
                download_url = 'https://www.biqukan.com' + child.a.get('href')
                download_name = child.string
                dl(download_url)
                index += 1
                sys.stdout.write("\r已下载:%.3f%%" % float(index / numbers))
				# \r要写在前面哦
                sys.stdout.flush()
file.close()