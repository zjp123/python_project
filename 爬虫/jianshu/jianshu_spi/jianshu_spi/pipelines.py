# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

#同步
class JianshuSpiPipeline(object):

    def __init__(self):

        datapar = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.con = pymysql.connect(**datapar)

        self.cur = self.con.cursor()
        self._sql = None



    def process_item(self, item, spider):

        self.cur.execute(self.sql, (item['title']))
        self.con.commit()

        return item


    @property
    def sql(self):

        if not self._sql:
            self._sql = """
            
                insert into artical (id, title) values(id, %s)
            """
            return self._sql

        return self._sql

#异步
class Youhuaban(object):
    def __init__(self):
        datapar = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }


        self.dbpool = adbapi.ConnectionPool('pymysql', **datapar)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """

                   insert into artical (id, title) values(id, %s)
               """
            return self._sql

        return self._sql

    def process_item(self, item, spider):

       defer = self.dbpool.runInteraction(self.insert_item, item)
       defer.addErrback(self.errhandle, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title']))

    def errhandle(self):
        print('发生错误了')