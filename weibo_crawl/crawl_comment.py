# coding=gbk

import requests
import urllib3
from bs4 import BeautifulSoup as BS
from lxml import etree
import time
from boom import Proxies
import random

urllib3.disable_warnings()


class Loginweibo(object):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    session.verify = False

    def __init__(self):
        self.username = '13218022128'
        self.password = '3_like_nitrome'
        self.session = Loginweibo.session

    def before_login(self):
        url = 'https://passport.weibo.cn/signin/login'
        params = {
            'entry': 'mweibo',
            'r': 'https://weibo.cn/pub/top?cat=star&pos=65',
            'backTitle': '(unable to decode value)',
            'vt': ''
        }
        headers = {
            'Referer': 'https://weibo.cn/pub/top?cat=star&pos=65&vt=',
            'Host': 'passport.weibo.cn',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
        }
        req = self.session.get(url=url, params=params, headers=headers)

    def login(self):
        url = 'https://passport.weibo.cn/sso/login'
        data = {
            'username': '13218022128',
            'password': '3_like_nitrome',
            'savestate': '1',
            'r': 'https://weibo.cn/pub/top?cat=star&pos=65',
            'ec': '0',
            'pagerefer': 'https://weibo.cn/pub/top?cat=star&pos=65&vt=',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2Fpub%2Ftop%3Fcat%3Dstar%26pos%3D65&backTitle=%CE%A2%B2%A9&vt='
        }
        self.session.post(url=url, headers=headers, data=data)

    def visit_my(self):
        self.login()
        print(id)
        url = 'https://weibo.cn/'
        headers = {
            'upgrade-insecure-requests': '1',
            'accept-encoding': 'gzip, deflate, br'
        }
        req = self.session.get(url=url, headers=headers)
        # print(req.text)

    def crawl_weibo(self):
        self.visit_my()
        url = 'https://weibo.cn/jiuguimoye?page=1'
        headers = {
            'upgrade-insecure-requests': '1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        req = self.session.get(url=url, headers=headers)
        bf = BS(req.text, features='lxml')
        motherfucker = bf.find_all('div', class_='c')
        for mother in motherfucker:
            etreei = etree.HTML(str(mother))
            text = etreei.xpath('//span[@class="ctt"]//text()')
            # if text:
            #     print(','.join(text))
            #     print('*' * 100)

    def crawl_comment(self, proxies_list):
        self.crawl_weibo()
        for i in range(1, 100):
            time.sleep(1)
            url = 'https://weibo.cn/comment/Hm4RM2MQl?&page=%s' % str(i)
            headers = {
                'upgrade-insecure-requests': '1',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
            }
            proxy = random.sample(proxies_list, 1)[0]
            res = self.session.get(url=url, headers=headers, proxies=proxy)
            bf = BS(res.text, features='lxml')
            motherfucker = bf.find_all('div', class_='c')
            for mother in motherfucker:
                etreei = etree.HTML(str(mother))
                text = etreei.xpath('//span[@class="ctt"]//text()')
                if text:
                    print(','.join(text))
                    print('*' * 30 + '你打球像蔡徐坤' + '*' * 30)

a = Loginweibo()
a.crawl_comment(Proxies().crawl_ip())
