import scrapy
from scrapy import Selector
from lianjiapro.items import lianjiaproItem
# import time
from json import loads
from lxml import etree
from bs4 import BeautifulSoup as BS
import re


class lianjiaproject(scrapy.Spider):
    name = 'ljpro'

    def __init__(self, **kwargs):
        self.allow_domains = ['lianjia.com']
        self.start_urls = ['https://www.lianjia.com/city/']
        self.xpath1 = '//div[@class="address"]/div[@class="houseInfo"]/a/text()'
        self.xpath2 = '//div[@class="address"]/div[@class="houseInfo"]/text()'
        self.xpath3 = '//div[@class="flood"]/div[@class="positionInfo"]/a/text()'
        self.xpath4 = '//div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()'
        self.xpath5 = '//div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price'
        self.cityxpath = '//div[@class="city_province"]/ul/li/a/@href'
        self.cityname = '//div[@class="city_province"]/ul/li/a/text()'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse1)

    def parse1(self, response):
        info = Selector(response)
        city_list = info.xpath(self.cityxpath).extract()
        city_names = info.xpath(self.cityname).extract()
        for (city_name, city_url) in zip(city_names, city_list):
            test_item = {}
            test_item['city_name'] = city_name
            test_url = city_url + '/ershoufang/pg1/' # 此处需要修正，部分城市无二手房信息，要设置if进行执行判断
            try:
                yield scrapy.Request(url=test_url, meta={'item': test_item, 'city_url': city_url}, callback=self.parse2)
            except Exception as e:
                print('step1:', e)

    def parse2(self, response):
        test_item = response.meta['item']
        city_url = response.meta['city_url']
        info = Selector(response)
        try:
            indexes = info.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
            index = loads(indexes[0])['totalPage']
            if 'bj' != re.findall('//(.*).lianjia', city_url)[0]:
                for i in range(1, int(index) + 1):  # 此处需要修正，部分城市房子不到3000套
                    # time.sleep(1)
                    url = city_url + '/ershoufang/pg%s/' % str(i)
                    yield scrapy.Request(url=url, meta={'item': test_item}, callback=self.parse3)
            else:
                for i in range(1, int(index) + 1):  # 此处需要修正，部分城市房子不到3000套
                    # time.sleep(1)
                    url = city_url + '/ershoufang/pg%s/' % str(i)
                    yield scrapy.Request(url=url, meta={'item': test_item}, callback=self.parse4)

        except Exception as e:
            print(test_item['city_name'], e)
            pass

    def parse3(self, response):
        info = Selector(response)
        item_list = []
        dict = {}
        community_names = info.xpath(self.xpath1).extract()
        # print(community_names)
        basic_infos = info.xpath(self.xpath2).extract()
        basic_infos = [i for i in basic_infos if i != '' and i != ' ']
        locations = info.xpath(self.xpath3).extract()
        total_prices = info.xpath(self.xpath4).extract()
        per_flats = info.xpath(self.xpath5).extract()

        for index in range(len(community_names)):
            test_item = response.meta['item']
            item = lianjiaproItem()
            item['city_name'] = test_item['city_name']
            item['community_name'] = community_names[index]
            # item['basic_info'] = basic_infos[index]
            item['location'] = locations[index]
            item['total_price'] = total_prices[index]
            item['per_flat'] = per_flats[index]
            elements = basic_infos[index].split('|')
            try:
                if u'别墅' not in elements[1]:
                    item['room_type'] = elements[1]
                    item['floor_space'] = re.findall(('\d+'), elements[2])[0]
                    item['toward'] = elements[3]
                    item['decoration_type'] = elements[4]
                else:
                    item['room_type'] = elements[2]
                    item['floor_space'] = re.findall(('\d+'), elements[3])[0]
                    item['toward'] = elements[4]
                    item['decoration_type'] = elements[1] + elements[5]
            except Exception as e:
                print(e)
                print('*' * 60)
                item['room_type'] = 'unknown'
                item['floor_space'] = 'unknown'
                item['toward'] = 'unknown'
                item['decoration_type'] = 'unknown'
            item_list.append(item)

        dict['info'] = item_list
        yield dict

    def parse4(self, response):
        info_extra = BS(response.body, features='lxml')
        info_soups = info_extra.find_all('div', class_='houseInfo')

        info = Selector(response)
        item_list = []
        dict = {}
        community_names = info.xpath(self.xpath1).extract()
        locations = info.xpath(self.xpath3).extract()
        total_prices = info.xpath(self.xpath4).extract()
        per_flats = info.xpath(self.xpath5).extract()

        for index in range(len(community_names)):
            test_item = response.meta['item']
            item = lianjiaproItem()
            item['city_name'] = test_item['city_name']
            item['community_name'] = community_names[index]
            # item['basic_info'] = basic_infos[index]
            item['location'] = locations[index]
            item['total_price'] = total_prices[index]
            item['per_flat'] = per_flats[index]

            preelements = info_soups[index]
            info_html = etree.HTML(str(preelements))
            info_result = info_html.xpath('//div/text()')
            elements = [i for i in info_result if i != '' and i != ' ']
            try:
                if u'别墅' not in elements[0]:
                    item['room_type'] = elements[0]
                    item['floor_space'] = re.findall(('\d+'), elements[1])[0]
                    item['toward'] = elements[2]
                    item['decoration_type'] = elements[3]
                else:
                    item['room_type'] = elements[1]
                    item['floor_space'] = re.findall(('\d+'), elements[2])[0]
                    item['toward'] = elements[3]
                    item['decoration_type'] = elements[0] + elements[4]
            except Exception as e:
                print(e)
                print('*' * 60)
                item['room_type'] = 'unknown'
                item['floor_space'] = 'unknown'
                item['toward'] = 'unknown'
                item['decoration_type'] = 'unknown'
            item_list.append(item)

        dict['info'] = item_list
        yield dict
