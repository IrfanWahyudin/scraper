# -*- coding: utf-8 -*-
import scrapy
import re
import json
class DetikSpider(scrapy.Spider):
    name = 'detik'
    allowed_domains = ['detik.com']
    start_urls = ['https://www.detik.com/']
    result_path = 'C:\\Users\\POJ\\Documents\\Projects\\scraper\\detik\\detik_crawler\\detik_crawler\\spiders\\results\\'

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
        author = response.selector.xpath('//div[@class="detail__author"]').extract()
        content = dict()

        if len(author) > 0:
            content['url'] = response.url
            content['title'] = ''
            content['author'] = self.cleanhtml(author[0])
            content['date'] = self.cleanhtml(response.selector.xpath('//div[@class="detail__date"]').extract()[0])
            content['detail_text'] = self.cleanhtml(response.selector.xpath('//div[@class="detail__body-text"]').extract()[0])
            self.write_file(content)




