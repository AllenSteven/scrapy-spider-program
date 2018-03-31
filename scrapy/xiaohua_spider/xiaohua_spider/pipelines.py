# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from twisted.enterprise import adbapi
import MySQLdb.cursors
import re


class JsonXiaohuaSpiderPipeline(object):
	def __init__(self):
		print("pipeline init **************************************************")
		self._filename = "F:/workspace/python/spider/scrapy/xiaohua_spider/xiaohua.json"
		self._fp = open(self._filename, "ab")
		
	def process_item(self, item, spider):
		print("pipeline **************************************************")
		line = "%s %s %s %s %s\n"%(
		item["userName"],
		item["userImg"],
		item["jokeText"],
		item["jokeImg"],
		item["jokeVideo"])
		
		print(line)
		print("***********json write***************")
		self._fp.write(line)
		#self._fp.close()
		return item

class DBXiaohuaSpiderPipeline(object):
	def __init__(self):
		self._db_pool = adbapi.ConnectionPool('MySQLdb', db = 'Dbxiaohua_2', user = 'test', passwd = 'test123', cursorclass = MySQLdb.cursors.DictCursor,use_unicode = True)
		
	def process_item(self, item, spider):
		print("*******DBXiaohuaSpiderPipeline process_item***************")
		query = self._db_pool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		print("*******DBXiaohuaSpiderPipeline process_item  end***************")
		return item
	
	def _conditional_insert(self, tx, item):
		print("********DBXiaohuaSpiderPipeline  _conditional_insert*******")
		values = (item["userName"],
		item["userImg"],
		item["jokeText"],
		item["jokeImg"],
		item["jokeVideo"])
		print("********DBXiaohuaSpiderPipeline  _conditional_insert middle*******")
		tx.execute("insert into joke_table(userName, userImg, jokeText, jokeImg, jokeVideo) values(%s, %s, %s, %s, %s)", values)
		print("********DBXiaohuaSpiderPipeline  _conditional_insert end*******")
	
	
	def handle_error(self, e):
		print("***************DBXiaohuaSpiderPipeline  handle_error*********************")
		print('error:'+str(e))
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		