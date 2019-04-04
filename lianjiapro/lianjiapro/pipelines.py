# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import re


class lianjiaproPipeline(object):

    def __init__(self):
        self.wb = Workbook()

    def process_item(self, item, spider):
        if item['city_name'] not in self.wb.get_sheet_names():
            self.sheet = self.wb.create_sheet(title=item['city_name'])
        elif item['city_name'] in self.wb.get_sheet_names():
            self.sheet = self.wb.get_sheet_by_name(item['city_name'])
        elements = item['basic_info'].split('|')
        room_type = elements[1]
        floor_space = re.findall(('\d+'), elements[2])[0]
        toward = elements[3]
        decoration_type = elements[4]
        self.sheet.append([item['community_name'], room_type, floor_space, toward,
                               decoration_type, item['location'],item['total_price'], item['per_flat']])
        self.wb.save('D:/Download/info.xlsx')
        return item
