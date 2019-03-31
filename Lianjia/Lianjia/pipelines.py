# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class LianjiaPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.sheet = self.wb.active

    def process_item(self, house_items, spider):
        for (k, item) in house_items.items():
            self.sheet.append([item['community_name'], item['basic_info'], item['location'],
                          item['total_price'], item['per_flat']])
        self.wb.save(r'D:\Download\nmsl.xlsx')
        return house_items
