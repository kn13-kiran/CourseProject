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
		print("???????????????????Dup")
		# Remove dup and already seen links
		if item.get('url') in self.crawled_links:
			raise DropItem("Duplicate link %s" % item.get('url'))
		else:
			self.crawled_links.add(item.get('url'))
			return item

class PageDataOutput(object):
	# Save successful output
	def process_item(self, item, spider):
		url =item.get('url')
		score= item.get('score')
		link_text = item.get('link_text')
		page_title = item.get('page_title')
		page_body = item.get('page_body')
		page_meta_data = link_text+page_title
		print("???url",url,"score",score,"linktext",page_body,",")
		line = url+","+str(score)+"\n"
		#print("Data Output",line)
		with open('finalresults/%s_all_links.txt' % spider.name, 'a+') as fp:
			fp.writelines([line])
		if item.get('score', 0) > 0.0:
			with open('finalresults/%s_menu_links.txt' % spider.name, 'a+') as fp:
				fp.writelines([line])

		#dumping sample seed data
		#category = "MenuPage "
		category="Other "
		globalIdx =random.randint(0,100000)
		#titlefilename = "menu_sample_"+str(globalIdx)+"_title"
		#contentfilename = "menu_sample_"+str(globalIdx)+"_content"
		titlefilename = "other_sample_"+str(globalIdx)+"_title"
		contentfilename = "other_sample_"+str(globalIdx)+"_content"

		page_meta_data = category+page_meta_data
		page_body = category+page_body
		#with open('dataset/sample/%s.txt' % titlefilename, 'a+') as fp:
		#	fp.writelines([page_meta_data])
		#with open('dataset/sample/%s.txt' % contentfilename, 'a+') as fp:
		#	fp.writelines([page_body])
