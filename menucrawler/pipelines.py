# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import random

class DuplicateLinkRemover(object):
	# Remove circular links
	def __init__(self):
		self.crawled_links = set()

	def process_item(self, item, spider):
		page_url =item.get('url')
		if page_url in self.crawled_links:
			raise DropItem("Link already examined %s" % page_url)
		else:
			self.crawled_links.add(page_url)
			return item

class PageDataOutput(object):
	def process_item(self, item, spider):
		url =item.get('url')
		score= item.get('score')
		line = url+","+str(score)+"\n"
		with open('finalresults/%s_all_links.txt' % spider.name, 'a+') as fp:
			fp.writelines([line])
		if item.get('score', 0) > 0.0:
			with open('finalresults/%s_menu_links.txt' % spider.name, 'a+') as fp:
				fp.writelines([line])

		#dumping sample seed data
		#link_text = item.get('link_text')
		#page_title = item.get('page_title')
		#page_body = item.get('page_body')
		#page_meta_data = link_text+page_title
		#category = "MenuPage "
		#category="Other "
		#page_meta_data = category+page_meta_data
		#page_body = category+page_body
		#with open('dataset/sample/%s.txt' % titlefilename, 'a+') as fp:
		#	fp.writelines([page_meta_data])
		#with open('dataset/sample/%s.txt' % contentfilename, 'a+') as fp:
		#	fp.writelines([page_body])
