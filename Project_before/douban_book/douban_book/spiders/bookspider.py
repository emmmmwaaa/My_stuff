# -*- coding: utf-8 -*-
import scrapy, re, time
from douban_book.items import DoubanBookItem


class BookSpider(scrapy.Spider):
    """docstring for BookSpider"""
    name = 'douban-book'
    allowed_domain = ['douban.com']
    start_urls = ['https://book.douban.com/top250']

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse1)
        for page in response.xpath('//div[@class="paginator"]/a'):
            link = page.xpath('@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse1)


    def parse1(self, response):
        m = response.xpath('//td[@valign="top"]')[0]
        for i in range(0,25):
            book = DoubanBookItem()
            book['name'] = m.xpath('//div[@class="pl2"]/a/@title').extract()[i]
            book['nums'] = m.xpath('//span[@class="pl"]/text()').extract()[i]
            book['ratings'] = m.xpath('//span[@class="rating_nums"]/text()').extract()[i]
            book['author'] = m.xpath('//p[@class="pl"]/text()').extract()[i]
            time.sleep(1)
            yield book







