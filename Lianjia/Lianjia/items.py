# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    community_name = scrapy.Field()
    basic_info = scrapy.Field()
    location = scrapy.Field()
    total_price = scrapy.Field()
    per_flat = scrapy.Field()

