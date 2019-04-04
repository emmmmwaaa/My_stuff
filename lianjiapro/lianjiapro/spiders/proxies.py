import requests, time
from lxml import etree
import threading
import urllib3, re

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
        self.test_list = []

    def crawl_ip(self):
        proxies_list = []
        thread_list = []
        for i in range(1, 3):
            time.sleep(5)
            url = 'https://www.xicidaili.com/nn/%s' % str(i)
            res = self.session.get(url=url)
            res_html = etree.HTML(res.text)
            # print(res.text)
            ip_addresses = res_html.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
            ip_ports = res_html.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
            ip_types = res_html.xpath('//table[@id="ip_list"]/tr/td[6]/text()')
            for (ip_address, ip_port, ip_type) in zip(ip_addresses, ip_ports, ip_types):
                ip_type = ip_type.lower()
                if ip_type == 'https':
                    proxy = {ip_type: ip_type + '://' + ip_address + ':' + ip_port}
                    proxies_list.append(proxy)
                    # print(proxy)
        for proxy in proxies_list:
            t = threading.Thread(target=self.utility_test, args=(proxy,))
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        print(self.test_list)
        return self.list

    # @staticmethod
    def utility_test(self, proxy):
        headers = {
            'Host': 'icanhazip.com',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        url = "http://icanhazip.com/"
        try:
            res = requests.get(url=url, headers=headers, proxies=proxy, timeout=3).text.strip('\n')
            self.test_list.append(proxy)
            test = re.findall(r'//(.*):', list(proxy.values())[0])[0]
            if res == test:
                # print(proxy)
                self.list.append(proxy)
        except Exception:
            return False