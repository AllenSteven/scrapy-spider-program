# -*- coding: utf-8 -*-
import scrapy


class MoneySpider(scrapy.Spider):
    name = 'money'
    allowed_domains = ['money.163.com']
    start_urls = ['http://money.163.com/']

    def parse(self, response):
        pass
