import urllib.request
import base64
import rsa, binascii
import time
import requests
import urllib3
from json import loads
import re
from lxml import etree
from openpyxl import Workbook

urllib3.disable_warnings()

class loginweibo(object):

    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate'
    })

    def __init__(self):
        self.user_name = '13218022128'
        self.pass_word = '3_like_nitrome'
        self.session = loginweibo.session
        self.session.get('https://login.sina.com.cn/signup/signin.php?entry=sso')

    def get_username(self):
        _username = urllib.request.quote(self.user_name)
        username = base64.encodebytes(_username.encode())[:-1]
        return username

    def get_password(self, servertime, nonce, pubkey):
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()

    def prelogin(self):
        prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php'
        pretime = int(round(time.time() * 1000))
        prelogin_params = {
            'entry': 'sso',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self.get_username(),
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.15)',
            '_': pretime
        }
        req1 = self.session.get(url=prelogin_url, params=prelogin_params)
        data_dict = loads(req1.text.split('(')[1].strip(')'))
        return pretime, data_dict

    def login(self):
        pretime, data_dict = self.prelogin()
        #print(data_dict)
        nowtime = int(round(time.time() * 1000))
        prelt = nowtime - pretime - int(data_dict['exectime'])
        login_url = 'https://login.sina.com.cn/sso/login.php'
        login_params = {
            'client': 'ssologin.js(v1.4.15)',
            '_': nowtime
        }
        login_data = {
            'entry': 'sso',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'pagerefer': 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)',
            'vsnf': '1',
            'su': self.get_username(),
            'service': 'sso',
            'servertime': data_dict['servertime'],
            'nonce': data_dict['nonce'],
            'pwencode': 'rsa2',
            'rsakv': data_dict['rsakv'],
            'sp': self.get_password(data_dict['servertime'], data_dict['nonce'], data_dict['pubkey']),
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': prelt,
            'returntype': 'TEXT'
        }
        req2 = self.session.post(url=login_url, data=login_data, params=login_params)
        extend_url1 = loads(req2.text)['crossDomainUrlList'][0].replace('\\', '')
        res = self.session.get(url=extend_url1)
        oops = res.text.strip().strip(');').strip('(')
        oops = loads(oops)
        #print(oops)
        id = oops['userinfo']['uniqueid']
        displayname = oops['userinfo']['displayname']
        return id, displayname

    def do_thing(self):
        wb = Workbook()
        sheet = wb.create_sheet('emmm', index=0)
        sheet.append(['url', '关注人数', '被关注', '发微博数'])
        id, displayname = self.login()
        home_url = 'https://weibo.com/u/' + id +'/home'
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Host': 'weibo.com',
            'Connection': 'keep-alive'
        }
        req = self.session.get(url=home_url, headers=headers)

        comment_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://weibo.com/1776448504/HcHWCpVF7?type=repost',
            'Host': 'weibo.com',
            'Connection': 'keep-alive'
        }
        url_list = []
        url_dict = {}
        list_count = 0
        for i in range(700, 800):
            comment_url2 = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4330288626179857&page=%s&__rnd=%s' % (str(i) ,str(int(round(time.time()))))
            comment_req = self.session.get(url=comment_url2, headers=comment_headers)
            time.sleep(0.5)
            comment_req.encoding = 'utf-8'
            req = loads(comment_req.content)['data']['html']
            req = req.replace('|', '').replace('｜', '')
            #注意哦，这个content里面有很多额外的有趣信息
            html = etree.HTML(req)
            # list = html.xpath('//div[@class="WB_text"]/span[@node-type="text"]/text()')
            # list2 = html.xpath('//div[@class="WB_text"]/a[@node-type="name"]')
            # for (i, j) in zip(list, list2):
            #     i = i.strip()
            #
            #     print(i)
            #     print(j.get('href'))
            # emmm = html.xpath('//div[@class="list_con"]/div[@class="WB_text"]/span[@node-type="text"]/text()')
            url_element = html.xpath('//div[@class="list_con"]/div[@class="WB_text"]/a[@node-type="name"]/@href')
            
            for url in url_element:
                if url not in url_list:
                    url_list.append(url)
                    url_dict[url] = self.weibo_user(url)
                    try:
                        sheet.append([str(url), url_dict[url][0], url_dict[url][1], url_dict[url][2]])
                    except Exception:
                        pass
                else:
                    list_count += 1
        print(list_count)
        #print(url_list)
        print(url_dict)
        wb.save('D:/新建文件夹/ikun.xlsx')




    def weibo_user(self, user_url):
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Host': 'weibo.com',
            'Connection': 'keep-alive'
        }
        req = self.session.get(url=user_url, headers=headers)
        pattern = re.compile(r'<strong class=\\"W_f18\\">(\d+)')
        num_list = pattern.findall(req.text)
        return num_list

a = loginweibo()
a.do_thing()
