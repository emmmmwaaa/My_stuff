# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class lianjiaproItem(scrapy.Item):
    city_name = scrapy.Field()
    community_name = scrapy.Field()
    # basic_info = scrapy.Field()
    location = scrapy.Field()
    total_price = scrapy.Field()
    per_flat = scrapy.Field()
    room_type = scrapy.Field()
    floor_space = scrapy.Field()
    toward = scrapy.Field()
    decoration_type = scrapy.Field()
