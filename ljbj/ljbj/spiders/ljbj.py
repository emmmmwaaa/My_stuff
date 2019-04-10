import scrapy
from scrapy import Selector
import re
from lxml import etree
from bs4 import BeautifulSoup as BS
from ljbj.items import LjbjItem


class ljbj(scrapy.Spider):
    name = 'ljbj'

    def __init__(self):
        self.allow_domains = ['lianjia.com']
        self.start_urls = ['https://bj.lianjia.com/chengjiao/']
        self.urlhead = 'https://bj.lianjia.com'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse1)

    def parse1(self, response):
        info = Selector(response)
        url_firsts = info.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        # 先爬取每个城区内部每个大概商圈的url
        for url_first in url_firsts[0:-2]:
            format_first = self.urlhead + url_first
            yield scrapy.Request(url=format_first, callback=self.parse2)
        for url_first in url_firsts[-2:]:
            yield scrapy.Request(url=url_first, callback=self.parse2_extra)

# 这是爬取北京地区的信息
    def parse2(self, response):
        list = []
        info = Selector(response)
        second_urls = info.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href').extract()
        area_names = info.xpath('//div[@data-role="ershoufang"]/div[2]/a/text()').extract()
        for (second_url, area_name) in zip(second_urls, area_names):
            if area_name not in list:
                list.append(area_name)
                real_url = self.urlhead + second_url
                yield scrapy.Request(url=real_url, meta={'item': area_name}, callback=self.parse3)

# 这是爬取河北地区的信息
    def parse2_extra(self, response):
        list = []
        info = Selector(response)
        second_urls = info.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href').extract()
        area_names = info.xpath('//div[@data-role="ershoufang"]/div[2]/a/text()').extract()
        for (second_url, area_name) in zip(second_urls, area_names):
            if area_name not in list:
                list.append(area_name)
                real_url = 'https://lf.lianjia.com' + second_url
                yield scrapy.Request(url=real_url, meta={'item': area_name}, callback=self.parse3)

    def parse3(self, response):
        info = Selector(response)
        area_name = response.meta['item']
        nums = int(info.xpath('//div[@class="total fl"]/span/text()').extract()[0].strip())
        pages = nums // 30 + 2
        for i in range(1, min(101, pages)):
            url = response.url + 'pg%s/' % str(i)
            yield scrapy.Request(url=url, meta={'item': area_name}, callback=self.parse4)

    def parse4(self, response):
        info = Selector(response)
        house_title_xpath = '//div[@class="info"]/div[@class="title"]/a/text()'
        url_xpath = '//div[@class="info"]/div[@class="title"]/a/@href'
        house_info_xpath = '//div[@class="address"]/div[@class="houseInfo"]/text()'
        dealDate_xpath = '//div[@class="address"]/div[@class="dealDate"]/text()'
        totalPrice_xpath = '//div[@class="address"]/div[@class="totalPrice"]//text()'
        unitPrice_xpath = '//div[@class="unitPrice"]//text()'

        urls = info.xpath(url_xpath).extract()
        house_titles = info.xpath(house_title_xpath).extract() # 需要解析出房间的户型和面积 利用split()
        house_infos = info.xpath(house_info_xpath).extract() # 房间朝向 是否精装 是否有电梯
        dealDates = info.xpath(dealDate_xpath).extract()
        totalPrices = info.xpath(totalPrice_xpath).extract()
        totalPrices = [i for i in totalPrices if i != u'万']
        unitPrices = info.xpath(unitPrice_xpath).extract()
        unitPrices = [i for i in unitPrices if i != u'元/平']

        if u'成交' in dealDates[0]:
            for index in range(len(urls)):
                item = LjbjItem()
                item['area_name'] = response.meta['item']
                house_title = house_titles[index].split()
                item['location'] = house_title[0]
                item['house_type'] = house_title[1]
                item['floor_space'] = house_title[2]
                house_info = house_infos[index].split('|')
                item['toward'] = house_info[0]
                item['decorate_type'] = house_info[1]
                yield scrapy.Request(url=urls[index], meta={'item': item}, callback=self.parse5)

        elif int(dealDates[0].split('.')[0]) >= 2017: # 这个地方注意一下 要把可爬取时间控制在两年之内
            for index in range(len(urls)):
                item = LjbjItem()
                item['area_name'] = response.meta['item']
                house_title = house_titles[index].split()
                item['location'] = house_title[0]
                item['house_type'] = house_title[1]
                item['floor_space'] = house_title[2]
                house_info = house_infos[index].split('|')
                item['toward'] = house_info[0]
                item['decorate_type'] = house_info[1]
                item['dealDate'] = dealDates[index]
                item['totalPrice'] = totalPrices[index]
                item['unitPrice'] = unitPrices[index]
                yield item

        else:
            pass

    def parse5(self, response):
        info = Selector(response)
        item = response.meta['item']
        item['dealDate'] = info.xpath('//div[@class="wrapper"]/span/text()').extract()[0]
        try:
            item['totalPrice'] = info.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()[0]
            item['unitPrice'] = info.xpath('//div[@class="price"]/b/text()').extract()[0]
        except:
            item['totalPrice'] = ''
            item['unitPrice'] = ''
        yield item


