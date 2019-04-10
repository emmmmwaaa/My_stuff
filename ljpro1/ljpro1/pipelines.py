# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class Ljpro1Pipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='Gxc072403666', database='test')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''create table user1 (area_name varchar(255), community_name varchar(255), room_type varchar(255), 
        floor_space float, toward varchar(255), decoration_type varchar(255), total_price float, per_flat float)''')

    def process_item(self, dict, spider):
        for item in dict['info']:
            self.cursor.execute('insert into user1 value (%s, %s, %s, %s, %s, %s, %s, %s)',
                                [item['area_name'], item['community_name'], item['room_type'], item['floor_space'],
                    item['toward'], item['decoration_type'], item['total_price'], item['per_flat']])
        self.conn.commit()
        return dict
