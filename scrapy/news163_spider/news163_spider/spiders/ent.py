# -*- coding: utf-8 -*-
import scrapy


class EntSpider(scrapy.Spider):
    name = 'ent'
    allowed_domains = ['ent.163.com']
    start_urls = ['http://ent.163.com/']

    def parse(self, response):
        pass
