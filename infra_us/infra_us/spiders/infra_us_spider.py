# -*- coding: utf-8 -*-

import logging.config

import scrapy
from scrapy import Selector, Request

from infra_us.items import DownHrefItem
from infra_us.settings import LOGGING


class InfraUsSpider(scrapy.Spider):
    name = 'infra_us'
    allowed_domains = ['hifld-dhs-gii.opendata.arcgis.com']
    logging.config.dictConfig(LOGGING)

    def start_requests(self):
        yield Request(url='https://hifld-dhs-gii.opendata.arcgis.com/', callback=self.parse)

    def parse(self, response):
        cla = Selector(response)
        cla_list = cla.xpath('//div[@class="categoryIconList"]/a')
        for row in cla_list:
            url = row.xpath('./@href').extract_first()
            cla_name = row.xpath('./div/text()').extract_first()
            yield Request(url=response.urljoin(url.strip()), callback=self.parse_final_href,
                          meta={'cla_name': cla_name.strip()})

    @staticmethod
    def parse_final_href(self, response):
        download = Selector(response)
        download_list = download.xpath('//li[@class="card card-summary item item-type-feature_service"]/div/'
                                       '@data-itemid').extract()
        url_list = []
        for row in download_list:
            url_list.append(response.urljoin('/datasets/' + row + '.csv'))
        down_href_item = DownHrefItem()
        down_href_item['cla_name'] = response.meta['cla_name']
        down_href_item['down_href'] = url_list
        yield down_href_item

