# -*- coding: utf-8 -*-
import scrapy
import json
import re

class KompasSpider(scrapy.Spider):
    name = 'kompas'
    allowed_domains = ['kompas.com']
    start_urls = ['http://kompas.com/']
    result_path = 'C:\\Users\\POJ\\Documents\\Projects\\scraper\\kompas\\kompas_crawler\\kompas_crawler\\spiders\\results\\'


    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext


    def parse(self, response):
        urls = response.xpath("//a/@href").extract()

        self.parse_detail(response)
        for url in urls:
            if 'http' in url[:4]:
                yield scrapy.Request(url=url, callback=self.parse)
        pass

    def write_file(self, content):
        f = open(self.result_path + content['url'].replace(':','_').replace('/','__') + '.json', 'w')
        f.write(json.dumps(content))
        f.close()

        return

    def parse_detail(self, response):
        author = response.selector.xpath('//div[@id="penulis"]/a/text()').extract()
        content = dict()

        if len(author) > 0:
            content['url'] = response.url
            content['title'] = self.cleanhtml(response.selector.xpath('//h1[@class="read__title"]/text()').extract()[0])
            content['author'] = self.cleanhtml(author[0])
            content['date'] = self.cleanhtml(response.selector.xpath('//div[@class="read__time"]/text()').extract()[0])
            content['detail_text'] = self.cleanhtml(response.selector.xpath('//div[@class="read__content"]').extract()[0])
            self.write_file(content)
