# -*- coding: utf-8 -*-
import mysql.connector


class lianjiaproPipeline(object):

    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='Gxc072403666', database='test')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''create table user (city_name varchar(255), community_name varchar(255), room_type varchar(255), floor_space varchar(255), toward varchar(255), decoration_type varchar(255),
                           location varchar(255), total_price varchar(255), per_flat varchar(255))''')


    def process_item(self, dict, spider):
        for item in dict['info']:
            self.cursor.execute('insert into user value (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                [item['city_name'], item['community_name'], item['room_type'], item['floor_space'],
                    item['toward'], item['decoration_type'], item['location'], item['total_price'], item['per_flat']])
        self.conn.commit()
        return dict

    def close_spider(self, spider):
        self.conn.close()

