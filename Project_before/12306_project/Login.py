from PIL import Image
import threading
from json import loads
from Utility import utility
from Const import API

class Login(object):
    session = utility.getSession()
    def __init__(self):
        self.session = Login.session

    def login(self):
        req1 = self.session.get(url=API.login_url)
        #print(req1.status_code)

        req2 = self.session.get(url=API.captcha_url)
        with open(u'D:/新建文件夹/code.png', 'wb') as f:
            f.write(req2.content)
        img = Image.open(u'D:/新建文件夹/code.png')
        img_thread = threading.Thread(target=img.show)
        img_thread.start()
        img_thread.join()
        data = input('请输入图片数据：')
        check_list = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
        codes = []
        groups = data.strip().split(',')
        for g in groups:
            codes.append(check_list[int(g) - 1])

        codes = ','.join(map(str, codes))
        data3 = {
            'answer': codes,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        req3 = self.session.post(url=API.captcha_check_url, data=data3)
        # if loads(req3.text)['result_code'] == '4':
        #    print('Success.')
        data4 = {
            'username': '13218022128',
            'password': '3_like_nitrome',
            'appid': 'otn'
        }
        req4 = self.session.post(url=API.login_url2, data=data4)
        self.uamtk = loads(req4.text)['uamtk']

        data5 = {'appid': 'otn'}
        req5 = self.session.post(url=API.uamtk_url, data=data5, allow_redirects=False)
        tk = loads(req5.text)["newapptk"]

        data6 = {'tk': tk}
        req6 = self.session.post(url=API.client_url, data=data6)
        self.apptk = loads(req6.text)["apptk"]
        #可以考虑在这里加增加一行有关联系人的数据
        #print(self.apptk)