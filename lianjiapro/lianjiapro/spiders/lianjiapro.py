import scrapy
from scrapy import Selector
from lianjiapro.items import lianjiaproItem
import time


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

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse1)

    def parse1(self, response):
        info = Selector(response)
        city_list = info.xpath(self.cityxpath).extract()
        for city_url in city_list:
            for i in range(1, 101):
                time.sleep(1)
                url = format_url = city_url + '/ershoufang/pg%s/' % str(i)
                yield scrapy.Request(url=url, callback=self.parse2)

    def parse2(self, response):
        info = Selector(response)
        house_items = {}

        community_names = info.xpath(self.xpath1).extract()
        basic_infos = info.xpath(self.xpath2).extract()
        locations = info.xpath(self.xpath3).extract()
        total_prices = info.xpath(self.xpath4).extract()
        per_flats = info.xpath(self.xpath5).extract()

        for index in range(len(community_names)):
            item = lianjiaproItem()
            item['community_name'] = community_names[index]
            item['basic_info'] = basic_infos[index]
            item['location'] = locations[index]
            item['total_price'] = total_prices[index]
            item['per_flat'] = per_flats[index]
            house_items[index] = item

        yield house_items

    def get_proxies(self):
        pass
