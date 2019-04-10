# -*- coding: utf-8 -*-
import scrapy


class LjbjSpider(scrapy.Spider):
    name = 'ljbj'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']

    def parse(self, response):
        pass
