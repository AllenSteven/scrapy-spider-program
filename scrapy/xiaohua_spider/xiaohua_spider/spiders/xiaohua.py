#!/usr/bin/env python
#-*-coding:utf-8-*-

import scrapy
#python2.7导入urllib,python3.x导入urllib.request : import urllib.request
import urllib
import os
from xiaohua_spider.items import XiaohuaSpiderItem
from scrapy.http import Request

#下载html源码
def saveHtml(response):
    url= response.url.split("/")
    print(url)
    filename = "xiaohua.html"
    print(filename)
    print("filename:"+str(filename))
    with open(filename,"wb") as f:
        f.write(response.body)

userimgs_dir = "F:/workspace/python/spider/scrapy/xiaohua_spider/users_images/"
jokeimgs_dir = "F:/workspace/python/spider/scrapy/xiaohua_spider/images/"
jokevideos_dir = "F:/workspace/python/spider/scrapy/xiaohua_spider/videos/"

def down_picture(url, srcpath, despath):
	if srcpath.startswith("http"):
		src = srcpath
	else:
		src = url+srcpath
		#src = os.path.join(url,srcpath) "http://www.xiaohua.com/" 
		#和"/Public/dz/images/portrait.png"合并最后得到的是/Public/dz/images/portrait.png，
		#因为多了一个/，所以合并时并没有得到想要的结果：http://www.xiaohua.com/Public/dz/images/portrait.png
	file_name = src.split('/')[-1]
	file_path = os.path.join(despath,file_name)
	#python2.7用urllib.urlretrieve，python3.x用urllib.request.urlretrieve，下载图像和视频。
	urllib.urlretrieve(src, file_path)
	return file_path
		
def get_username(content, item):
	print("get_username-----------------------")
	#.点号表示当前节点
	users = content.xpath('.//div[@class="one-cont-font clearfix"]/i/text()').extract()
	print("user len:"+str(len(users)))
	if users:
		item["userName"] = users[0].encode('utf-8')
	else:
		item["userName"] = None
		
	print("item['username']:%s"%(item["userName"].decode("utf-8")))

def get_userimg(url, content, item):
	print("get_userimg-----------------------")
	userimgs = content.xpath('.//div[@class="one-cont-font clearfix"]/em/img/@data-original').extract()
	print("userimgs len:%d"%len(userimgs))
	if userimgs:
		userimg = down_picture(url, userimgs[0], userimgs_dir)
		item["userImg"] = userimg.encode('utf-8')
	else:
		item["userImg"] = None
	
	print("item['userImg']:%s"%(item["userImg"]))
	
def get_joketext(content, item):
	print("get_joketext-----------------------")
	jokes = content.xpath('.//p[@class="fonts"]/a/text()').extract()
	print("jokes len:"+str(len(jokes)))
	if jokes:
		item["jokeText"] = jokes[0].strip().encode('utf-8')
	else:
		item["jokeText"] = None
	
	print("item['jokeText']:%s"%(item["jokeText"].decode("utf-8")))
	
def get_jokeimg(url, content, item):
	print("get_jokeimg-----------------------")
	jokeimgs = content.xpath('.//div[@class="imgs clearfix"]/div/img/@data-original').extract()
	if jokeimgs:
		jokeimg = down_picture(url, jokeimgs[0],jokeimgs_dir)
		item["jokeImg"] = jokeimg.encode('utf-8')
	else:
		item["jokeImg"] = None
		
	print("item['jokeImg']:%s"%(item["jokeImg"]))

def get_jokevideo(url,content, item):
	print("get_jokevideo-----------------------")
	jokevideos = content.xpath('.//div[@class="videos vid"]/video/source/@src').extract()
	print("jokevideos len:"+str(len(jokevideos)))
	if jokevideos:
		jokevideo = down_picture(url, jokevideos[0],jokevideos_dir)
		item["jokeVideo"] = jokevideo.encode('utf-8')
	else:
		item["jokeVideo"] = None
	print("item['jokeVideo']:%s"%(item["jokeVideo"]))
	
class XiaoHuaSpider(scrapy.Spider):
    name = "xiaohua"
    allowed_domains = ["xiaohua.com"]
    start_urls = [
	"http://www.xiaohua.com/index/index/type/0/p/2.html",
	"http://www.xiaohua.com/index/index/type/1/p/2.html",
	"http://www.xiaohua.com/index/index/type/2/p/2.html",
	"http://www.xiaohua.com/index/index/type/3/p/2.html"
	]
	
    def parse(self,response):
		current_url = response.url
		print("url:"+str(current_url))
		item = XiaohuaSpiderItem()
		saveHtml(response)
		div_contents = response.xpath('//div[@class="one-cont"]')
		print(len(div_contents))
	
		for content in div_contents:
			#get username and userimg
			print("users-----------------------")
			get_username(content, item)
			
			print("userimgs-----------------------")
			get_userimg(response.url, content, item)
			
			print("jokes-----------------------")
			get_joketext(content, item)
			
			print("jokeimgs-----------------------")
			get_jokeimg(response.url, content, item)
			
			print("jokevideos-----------------------")
			get_jokevideo(response.url, content, item)
			
			print("yield item &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
			#yield item必须放在parse函数中。
			yield item
		
		print("urls-------------------------")
		urls = response.xpath('/div[@class="content"]/div[@class="more"]/a/@href').extract()
		#print(urls)
		for url in urls:
			print(url)
			print(type(response.url))
			if not url.startswith(response.url):# and
				url_ab = response.url
				print(url_ab)
			if  url.endswith("/p/2.html"):
				print("iiiii")
				yield Request(url_ab, callback = self.parse)
		