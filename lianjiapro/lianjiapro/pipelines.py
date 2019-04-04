# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class lianjiaproPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.sheet = self.wb.active
        self.sheet.append(['city_name', 'community_name', 'room_type', 'floor_space', 'toward', 'decoration_type',
                           'location', 'total_price', 'per_flat'])

    def process_item(self, dict, spider):
        for item in dict['info']:
            # elements = item['basic_info'].split('|')
            # try:
            #     room_type = elements[1]
            #     floor_space = re.findall(('\d+'), elements[2])[0]
            #     toward = elements[3]
            #     decoration_type = elements[4]
            # except IndexError:
            #     room_type = ''
            #     floor_space = ''
            #     toward = ''
            #     decoration_type = ''
            self.sheet.append([item['city_name'], item['community_name'], item['room_type'], item['floor_space'],
                    item['toward'], item['decoration_type'], item['location'],item['total_price'], item['per_flat']])

        self.wb.save('D:/Download/info.xlsx')
        return dict
