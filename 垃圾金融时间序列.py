
import requests, urllib3, time
from lxml import etree
from openpyxl import Workbook

urllib3.disable_warnings()
session = requests.session()
session.headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3719.0 Safari/537.36',
}
session.verify = False
list = ['519697', '540006', '519712', '519732', '000083', '519700', '070032', '000410', '163415', '110011']
wb = Workbook()

for (i, k) in zip(list, range(10)):
    sheet = wb.create_sheet(list[k], index=k)
    sheet.append(['time', 'NAV', 'Accumulated Net', 'Volatility'])
    for j in range(21):
        time.sleep(0.5)
        url = 'http://quotes.money.163.com/fund/jzzs_' + i + '_' + str(j) + '.html?start=2014-03-22&end=2019-03-21&sort=TDATE&order=desc'
        req = session.get(url=url)
        html = etree.HTML(req.text)
        ele1 = html.xpath('//table[@class="fn_cm_table"]/tbody/tr/td[1]/text()')
        ele2 = html.xpath('//table[@class="fn_cm_table"]/tbody/tr/td[2]/text()')
        ele3 = html.xpath('//table[@class="fn_cm_table"]/tbody/tr/td[3]/text()')
        ele4 = html.xpath('//table[@class="fn_cm_table"]/tbody/tr/td[4]/span/text()')
        for (a, b, c, d) in zip(ele1, ele2, ele3, ele4):
            sheet.append([str(a), float(b), float(c), str(d)])
wb.save('D:/新建文件夹/sample1.xlsx')
