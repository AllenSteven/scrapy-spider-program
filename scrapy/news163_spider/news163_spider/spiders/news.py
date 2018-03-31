# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

def saveHtml(response):
    url= response.url.split("/")
    print(url)
    filename = "news.html"
    print(filename)
    print("filename:"+str(filename))
    with open(filename,"wb") as f:
        f.write(response.body)

URL = 'http://www.163.com/'
class NewsSpider(scrapy.Spider):
	name = 'news'
	#allowed_domains = ['news.163.com']
	start_urls = ['http://news.163.com/']
	
	def get_head_news(self, response):
		title = response.xpath('//div[@id="epContentLeft"]/h1/text()').extract()
		if title:
			title = title[0]
		else:
			title = None
			print("no title error , url: %s "%response.url)
		post_time = response.xpath('//div[@id="epContentLeft"]/div[@class="post_time_source"]/text()').extract()
		if post_time:
			post_time = post_time[0].strip()[:20]
		else:
			post_time = None
			print("no post_time error , url: %s "%response.url)
		post_source = response.xpath('//div[@id="epContentLeft"]/div[@class="post_time_source"]/a/text()').extract()
		if post_source:
			post_source = post_source[0]
		else:
			post_source = None
			print("no post_source error , url: %s "%response.url)
		new_texts = response.xpath('//div[@id="epContentLeft"]/div[@class="post_body"]/div[@id="endText"]')
		otitle = new_texts.xpath('./p[@class="otitle"]/text()').extract()
		if otitle:
			otitle = otitle[0].strip()
		else:
			otitle = None
		video = new_texts.xpath('.//div[@class="video-wrapper"]//video').extract()
		texts = new_texts.xpath('./p/text()').extract()
		print(title)
		print(post_time)
		print(post_source)
		print(otitle)
		print(video)
		#for text in texts:
		#	print(text)
	
	def get_special_news(self, response):
		print("**********get_special_news**************")
		#print(response.url)
		imglink = response.xpath('//div[@id="renjian_banner"]/img/@src').extract()
		
		if imglink:
			imglink = imglink[0]
		else:
			imglink = None
		print(imglink)
		title_text = response.xpath('//div[@class="bannertext"]/h1/text()').extract()
		
		if title_text:
			title_text = title_text[0]
		else:
			title_text = None
		print(title_text)
		post_time = response.xpath('//div[@class="bannertext"]//div[@class="pub_time"]/text()').extract()
		
		if post_time:
			post_time = post_time[0]
		else:
			post_time = None
		print(post_time)
		author_img = response.xpath('//div[@id="rj_author"]//div[@class="author_img"]/img/@src').extract()
		print(author_img)
		author_name = response.xpath('//div[@id="rj_author"]//div[@class="author_txt"]/p/span[@class="name"]/text()').extract()
		print(author_name)
		author_work = response.xpath('//div[@id="rj_author"]//div[@class="author_txt"]/p/text()').extract()
		print(author_work)
		content = response.xpath('//div[@id="rj_bd"]//div[@id="endText"]/p/text()').extract()
		#print(content)
	
	def get_special_news_caozhi(self, response):
		print("*******************get_special_news_caozhi****************************")
		print(response.url)
		title = response.xpath('//div[@class="cc_bd_w1000"]/div[@class="brief"]/h1/text()').extract()
		if title:
			title = title[0]
		else:
			title = None
		post_time = response.xpath('//div[@class="cc_bd_w1000"]/div[@class="brief"]/div[@class="pub_time"]/text()').extract()
		if post_time:
			post_time = post_time[0]
		else:
			post_time = None
		intro = response.xpath('//div[@class="cc_bd_w1000"]//div[@class="cc_main"]/div[@class="intro"]/p/text()').extract()
		if intro:
			intro = intro[0]
		else:
			intro = None
		content = response.xpath('//div[@class="cc_bd_w1000"]//div[@class="cc_main"]/div[@class="endText"]/p/text()').extract()		
		#if content:
		#	content = content[]
		
		
		print(title)
		print(post_time)
		print(intro)
		print(content)
		
	def get_stream_data(self, response):
		print("*******************get_stream_data************************")
		data_rows = response.xpath('//li[@class="newsdata_item current"]')
		print(data_rows)
		print(len(data_rows))
		
	def parse(self, response):
		print("***************parse url**************************")
		print(response.url)
		#headnews = response.xpath('//div[@class="ns_area clearfix index_main"]//div[@class="main_center_news"]//div[@id="js_top_news"]//a/@herf')
		#get head news
		print("***************head news***********************")
		headnews = response.xpath('//div[@class="main_center_news"]//div[@id="js_top_news"]//a')
		print(len(headnews))
		print(headnews)
		for headnew in headnews:
			
			title = headnew.xpath('./text()').extract()
			if title:
				title = title[0]
			else:
				title = None
			link = headnew.xpath('./@href').extract()
			if link:
				link = link[0]
			else:
				link = None
				
			print(link)
			print(title)
			print("******************")
			yield Request(link, callback=self.get_head_news)
		
		
		print("****************special news*********************")
		#get special news
		special_news = response.xpath('//div[@class="mod_netes_origina"]//div[@class="focus_body"]//li/a[@class="photo"]')
		print(len(special_news))
		for special_new in special_news:
			link = special_new.xpath('./@href').extract()
			if link:
				link = link[0]
			else:
				link = None
			title = special_new.xpath('./@title').extract()
			print(title)
			print(link)
			if link.startswith("http://renjian"):
				yield Request(link, callback = self.get_special_news)
			else:
				yield Request(link, callback = self.get_special_news_caozhi)
		
		print("*****************newsdata_naw*************************")
		links = response.xpath('//div[@class="newsdata_nav"]//li[@class="nav_item"]/a/@href').extract()
		print(len(links))
		print(links)
		
		print("***************http:163.com***********************")
		index_heads = response.xpath('//div[@class="index2016_content"]//div[@class="index_head"]//div[@class="bd"]//ul/li/a/@href').extract()
		print(index_heads)
		print(response.url)
		for head in index_heads:
			if not head.startswith(URL):
				yield Request(head, callback = self.parse)
				pass
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
