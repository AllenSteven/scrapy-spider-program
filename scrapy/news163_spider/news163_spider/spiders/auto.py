# -*- coding: utf-8 -*-
import scrapy


class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['auto.163.com']
    start_urls = ['http://auto.163.com/']

    def parse(self, response):
        pass
