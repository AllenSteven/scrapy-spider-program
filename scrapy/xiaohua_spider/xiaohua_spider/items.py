# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userName = scrapy.Field()
    userImg = scrapy.Field()
    jokeText = scrapy.Field()
    jokeImg = scrapy.Field()
    jokeVideo = scrapy.Field()

