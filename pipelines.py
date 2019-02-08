# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from jobsearch.items import JobsearchItem
import pymongo
import pymysql

class JobsearchPipeline(object):

    def __init__(self):
        self.headers = list(JobsearchItem.fields.keys())
        self.file = open('/Users/cb/Downloads/Project/Project_crawler job/Project/Result Data/jobsearch.csv', 'a', encoding='utf-8')
        self.f_csv = csv.DictWriter(self.file, self.headers)
        self.f_csv.writeheader()

    def process_item(self, item, spider):
        self.f_csv.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()


class JobSearchMongoPipeline(object):

    collection_name = 'jobsearch'

    def __init__(self, mongo_url, mongo_db, replicaset):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'job'),
            replicaset=crawler.settings.get('REPLICASET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url, replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item

class JobSearchMysqlPipeline(object):

    def __init__(self, mysql_host, mysql_port, mysql_db, mysql_table, mysql_user, mysql_pass):
        self.mysql_table = mysql_table
        self.client = pymysql.connect(host=mysql_host,
                                      port=mysql_port,
                                      db=mysql_db,
                                      user=mysql_user,
                                      passwd=mysql_pass)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_URI'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE'),
            mysql_table=crawler.settings.get('MYSQL_TABLE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_pass=crawler.settings.get('MYSQL_PASS')

        )

    def open_spider(self, spider):
        self.cur = self.client.cursor()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        keys = ','.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) '.format(table=self.mysql_table, keys=keys, values=values)

        self.cur.execute(sql, tuple(item.values()))
        self.client.commit()
        return item



