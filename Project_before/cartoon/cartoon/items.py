# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy

class ComicItem(scrapy.Item):
    dir_name = scrapy.Field()
    link_url = scrapy.Field()
    img_url = scrapy.Field()
    image_paths = scrapy.Field()
