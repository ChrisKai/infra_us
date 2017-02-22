# -*- coding: utf-8 -*-

import logging
import json

import redis

from infra_us.settings import REDIS_HOST, REDIS_PORT
from items import DownHrefItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class InfraUsPipeline(object):
    def process_item(self, item, spider):
        return item


class RedisPipeline(object):
    def __init__(self):
        self.redis_obj = redis.Redis(REDIS_HOST, REDIS_PORT)
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        if isinstance(item, DownHrefItem):
            data = json.dumps({item['cla_name']: item['down_href']})
            down_href = self.redis_obj.lrange('down_href', 0, -1)
            if not down_href:
                self.redis_obj.rpush('down_href', data)
                self.logger.info(u'添加新的下载链接成功\n')
            else:
                if data in down_href:
                    self.logger.info(u'链接已存在，忽略此链接\n')
                else:
                    self.redis_obj.rpush('down_href', data)
                    self.logger.info(u'添加新的下载链接成功\n')
        else:
            self.logger.error(u'不存在此类别item\n')
        return item
