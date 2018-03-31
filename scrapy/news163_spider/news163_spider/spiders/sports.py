# -*- coding: utf-8 -*-
import scrapy


class SportsSpider(scrapy.Spider):
    name = 'sports'
    allowed_domains = ['sports.163.com']
    start_urls = ['http://sports.163.com/']

    def parse(self, response):
        pass
