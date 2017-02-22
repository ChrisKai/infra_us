### 入口页
    cla = scrapy.Selector(response)
    cla.xpath('//div[@class="categoryIconList"]/a/@href').extract()
### 下载链接获取页
    download = Selector(response)
    download_list = download.xpath('//li[@class="card card-summary item item-type-feature_service"]/div/@data-itemid').extract()