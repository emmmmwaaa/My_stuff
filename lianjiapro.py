# -*- coding: utf-8 -*-
import scrapy


class LianjiaproSpider(scrapy.Spider):
    name = 'lianjiapro'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']

    def parse(self, response):
        pass
