import scrapy
from scrapy import Selector
import re
from lxml import etree
from bs4 import BeautifulSoup as BS
from ljpro1.items import Ljpro1Item

class ljpro1(scrapy.Spider):
    name = 'ljpro1'

    def __init__(self):
        self.allow_domains = ['lianjia.com']
        self.start_urls = ['https://bj.lianjia.com/ershoufang/']
        self.url_header = 'https://bj.lianjia.com'
        self.xpath1 = '//div[@class="address"]/div[@class="houseInfo"]/a/text()'
        self.xpath2 = '//div[@class="address"]/div[@class="houseInfo"]/text()'
        # self.xpath3 = '//div[@class="flood"]/div[@class="positionInfo"]/a/text()'
        self.xpath4 = '//div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()'
        self.xpath5 = '//div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price'
        self.name_list = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse1)

    def parse1(self, response):
        info = Selector(response)
        url_distincts = info.xpath('//div[@class="sub_nav section_sub_nav"]/a/@href').extract()
        # distincts = info.xpath('//div[@class="sub_nav section_sub_nav"]/a/text()').extract()
        for url in url_distincts:
            format_url = self.url_header + url
            yield scrapy.Request(url=format_url, callback=self.parse4)

    def parse4(self, response):
        format_info = Selector(response)
        real_urls = format_info.xpath('//div[@class="sub_sub_nav section_sub_sub_nav"]/a/@href').extract()
        area_names = format_info.xpath('//div[@class="sub_sub_nav section_sub_sub_nav"]/a/text()').extract()
        for (area_name, real_url) in zip(area_names, real_urls):
            if area_name not in self.name_list:
                self.name_list.append(area_name)
                exactly_url = self.url_header + real_url
                yield scrapy.Request(url=exactly_url, meta={'item': area_name}, callback=self.parse2)

    def parse2(self, response):
        info = Selector(response)
        area_name = response.meta['item']
        nums = int(info.xpath('//h2[@class="total fl"]/span/text()').extract()[0].strip())
        pages = nums // 30 + 2
        for i in range(1, min(101, pages)):
            url = response.url + 'pg%s' % str(i)
            yield scrapy.Request(url=url, meta={'item': area_name}, callback=self.parse3)

    def parse3(self, response):
        info_extra = BS(response.body, features='lxml')
        info_soups = info_extra.find_all('div', class_='houseInfo')
        info = Selector(response)
        item_list = []
        dict = {}
        community_names = info.xpath(self.xpath1).extract()
        # locations = info.xpath(self.xpath3).extract()
        total_prices = info.xpath(self.xpath4).extract()
        per_flats = info.xpath(self.xpath5).extract()
        for index in range(len(community_names)):
            item = Ljpro1Item()
            item['area_name'] = response.meta['item']
            item['community_name'] = community_names[index]
            # item['basic_info'] = basic_infos[index]
            # item['location'] = locations[index]
            item['total_price'] = float(total_prices[index])
            item['per_flat'] = float(per_flats[index])

            preelements = info_soups[index]
            info_html = etree.HTML(str(preelements))
            info_result = info_html.xpath('//div/text()')
            elements = [i for i in info_result if i != '' and i != ' ']
            try:
                if u'别墅' not in elements[0]:
                    item['room_type'] = elements[0]
                    item['floor_space'] = float(re.findall(('\d+'), elements[1])[0])
                    item['toward'] = elements[2]
                    item['decoration_type'] = elements[3]
                else:
                    item['room_type'] = elements[1]
                    item['floor_space'] = float(re.findall(('\d+'), elements[2])[0])
                    item['toward'] = elements[3]
                    item['decoration_type'] = elements[0] + elements[4]
            except Exception as e:
                print(e)
                print('*' * 60)
                item['room_type'] = ''
                item['floor_space'] = 0
                item['toward'] = ''
                item['decoration_type'] = ''
            item_list.append(item)

        dict['info'] = item_list
        yield dict




