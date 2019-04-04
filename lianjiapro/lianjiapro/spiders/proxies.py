import requests, time
import threading
import urllib3, re, random
from lxml import etree
from fake_useragent import UserAgent

urllib3.disable_warnings()

class Proxies(object):

    def __init__(self):
        self.list = []
        self.test_list = []

    def precrawl_ip(self):
        thread_list = []
        for i in range(1, 3):
            time.sleep(2)
            url = 'https://www.xicidaili.com/nn/%s' % str(i)
            proxies_list = self.lxml_ip(url=url)
            for proxy in proxies_list:
                t = threading.Thread(target=self.utility_test, args=(proxy,))
                thread_list.append(t)
                t.start()
        for t in thread_list:
            t.join()
                # print(self.test_list)
        return self.list

    def lxml_ip(self, url, proxies=None):
        ua = UserAgent()
        proxies_list = []
        headers = {
            'Host': 'www.xicidaili.com',
            'Referer': 'https://www.xicidaili.com/nn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua.random
        }
        res = requests.get(url=url, headers=headers, verify=False, proxies=proxies)
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
        return proxies_list

    def crawl_ip(self):
        preproxies_list = self.precrawl_ip()
        # print(preproxies_list)
        thread_list = []
        for i in range(3, 8):
            time.sleep(1)
            url = 'https://www.xicidaili.com/nn/%s' % str(i)
            proxies = random.choice(preproxies_list)
            proxies_list = self.lxml_ip(url=url, proxies=proxies)
            for proxy in proxies_list:
                t = threading.Thread(target=self.utility_test, args=(proxy,))
                thread_list.append(t)
                t.start()
        for t in thread_list:
            t.join()
            # print(self.test_list)
        return self.list

    # @staticmethod
    def utility_test(self, proxy):
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        url = 'https://www.whatismybrowser.com/detect/what-is-my-ip-address'
        try:
            res = requests.get(url=url, headers=headers, proxies=proxy, timeout=3).text
            self.test_list.append(proxy)
            # print('1\n', res, '\n')
            html = etree.HTML(res)
            res1 = html.xpath('//div[@class="detected_result"]//div[@class="value"]/text()')[0]
            # print('2\n', res1, '\n')
            test = re.findall(r'//(.*):', list(proxy.values())[0])[0]
            if res1 == test:
                # print(proxy)
                self.list.append(proxy)
        except Exception:
            return False

a = Proxies()
print(a.crawl_ip())