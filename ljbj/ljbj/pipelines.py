# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class LjbjPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='Gxc072403666', database='test')
        self.cursor = self.conn.cursor()
        self.cursor.execute('drop table if exists user2')
        self.cursor.execute('''create table user2 (area_name varchar(255),
                                location varchar(255),
                                house_type varchar(255),
                                floor_space varchar(255),
                                toward varchar(255),
                                decorate_type varchar(255),
                                dealDate varchar(255),
                                totalPrice varchar(255),
                                unitPrice varchar(255))
        ''')

    def process_item(self, item, spider):
        self.cursor.execute(
            'insert into user2 value (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [item['area_name'], item['location'],item['house_type'], item['floor_space'], item['toward'], item['decorate_type'], item['dealDate'], item['totalPrice'], item['unitPrice']])

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()

