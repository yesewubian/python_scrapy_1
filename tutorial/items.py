# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    title = scrapy.Field()
    introduce = scrapy.Field()
    addr = scrapy.Field()
    tel = scrapy.Field()
    olink = scrapy.Field()
    otime = scrapy.Field()
    lysj = scrapy.Field()
    jtzn = scrapy.Field()
    ts = scrapy.Field()
