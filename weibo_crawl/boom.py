import requests
import urllib3
from lxml import etree
import time
import threading

urllib3.disable_warnings()


class Proxies(object):

    def __init__(self):
        session = requests.Session()
        session.headers = {
            'Host': 'www.xicidaili.com',
            'Referer': 'https://www.xicidaili.com/nn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        session.verify = False
        self.session = session
        self.list = []

    def crawl_ip(self):
        proxies_list = []
        for i in range(1, 2):
            time.sleep(1)
            url = 'https://www.xicidaili.com/nn/%s' % str(i)
            res = self.session.get(url=url)
            res_html = etree.HTML(res.text)
            ip_addresses = res_html.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
            ip_ports = res_html.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
            ip_types = res_html.xpath('//table[@id="ip_list"]/tr/td[6]/text()')
            for (ip_address, ip_port, ip_type) in zip(ip_addresses, ip_ports, ip_types):
                ip_type = ip_type.lower()
                proxy = {ip_type: ip_type + '://' + ip_address + ':' + ip_port}
                proxies_list.append(proxy)
        for proxy in proxies_list:
            t = threading.Thread(target=self.utility_test, args=(proxy,))
            t.start()
        t.join()
        return self.list

    # @staticmethod
    def utility_test(self, proxy):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        url = 'https://www.baidu.com'
        try:
            requests.get(url=url, headers=headers, proxies=proxy, timeout=1)
            self.list.append(proxy)
        except Exception:
            return False