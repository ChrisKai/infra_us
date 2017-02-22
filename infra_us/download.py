# -*- coding: utf-8 -*-

import os
import json
import urllib
import logging
import logging.config

import redis

from infra_us.settings import REDIS_HOST, REDIS_PORT, LOGGING


class Download:
    def __init__(self):
        self.redis_obj = redis.Redis(REDIS_HOST, REDIS_PORT)
        logging.config.dictConfig(LOGGING)
        self.logger = logging.getLogger(__name__)

    def download_file(self):
        down_href = self.redis_obj.lrange('down_href', 0, -1)
        for row in down_href:
            data = json.loads(row)
            for k, v in data.items():
                store_path = os.path.dirname(os.path.abspath(__name__)) + '/download_file/' + k.replace(' ', '_')
                if not os.path.exists(store_path):
                    os.makedirs(store_path)
                    self.logger.info(u'成功创建目录：%s' % store_path)
                for url in v:
                    urllib.urlretrieve(url, os.path.join(store_path, url.split('/')[-1]))
                    self.logger.info(u'下载文件成功：%s' % url.split('/')[-1])

if __name__ == '__main__':
    download = Download()
    download.download_file()
