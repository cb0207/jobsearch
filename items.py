# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    postn_name = scrapy.Field()
    postn_web = scrapy.Field()
    postn_area = scrapy.Field()
    postn_adds = scrapy.Field()
    postn_salary = scrapy.Field()
    postn_experience = scrapy.Field()
    postn_edu = scrapy.Field()
    postn_numHire = scrapy.Field()
    postn_benifit = scrapy.Field()
    com_name = scrapy.Field()
    com_web = scrapy.Field()
    com_simInfo = scrapy.Field()
    post_date = scrapy.Field()
    resource = scrapy.Field()

