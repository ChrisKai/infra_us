# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfraUsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DownHrefItem(scrapy.Item):
    cla_name = scrapy.Field()  # 存储分类名
    down_href = scrapy.Field()  # 存储下载链接