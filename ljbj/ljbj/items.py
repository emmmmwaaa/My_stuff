# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LjbjItem(scrapy.Item):
    area_name = scrapy.Field()
    location = scrapy.Field()
    house_type = scrapy.Field()
    floor_space = scrapy.Field()
    toward = scrapy.Field()
    decorate_type = scrapy.Field()
    dealDate = scrapy.Field()
    totalPrice = scrapy.Field()
    unitPrice = scrapy.Field()
