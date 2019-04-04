import scrapy
from scrapy import Selector
from lianjiapro.items import lianjiaproItem
import time
from json import loads

class lianjiaproject(scrapy.Spider):
    name = 'ljpro'

    # 只能爬取前3k的数据，可以考虑通过限定数据【例如通过控制房价在一定范围之内】来进行计算

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
            # time.sleep(1)
            test_item['city_name'] = city_name
            test_url = city_url + '/ershoufang/pg1/' # 此处需要修正，部分城市无二手房信息，要设置if进行执行判断
            yield scrapy.Request(url=test_url, meta={'item':test_item, 'city_url':city_url}, callback=self.parse2)

    def parse2(self, response):
        test_item = response.meta['item']
        city_url = response.meta['city_url']
        info = Selector(response)
        try:
            indexes = info.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
            index = loads(indexes[0])['totalPage']
            for i in range(1, int(index)+1): # 此处需要修正，部分城市房子不到3000套
                # time.sleep(1)
                url = city_url + '/ershoufang/pg%s/' % str(i)
                yield scrapy.Request(url=url, meta={'item': test_item}, callback=self.parse3)
        except Exception as e:
            print(e)
            print(test_item['city_name'])
            pass

    def parse3(self, response):
        info = Selector(response)
        # list = []
        community_names = info.xpath(self.xpath1).extract()
        # print(community_names)
        basic_infos = info.xpath(self.xpath2).extract()
        locations = info.xpath(self.xpath3).extract()
        total_prices = info.xpath(self.xpath4).extract()
        per_flats = info.xpath(self.xpath5).extract()

        for index in range(len(community_names)):
            test_item = response.meta['item']
            item = lianjiaproItem()
            item['city_name'] = test_item['city_name']
            item['community_name'] = community_names[index]
            item['basic_info'] = basic_infos[index]
            item['location'] = locations[index]
            item['total_price'] = total_prices[index]
            item['per_flat'] = per_flats[index]
            yield item