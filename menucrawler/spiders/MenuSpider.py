# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from menucrawler.PageData import PageData
import time
import logging
from scrapy.http import Request
#from classifier import MenuClassfier
from bs4 import BeautifulSoup
from menu_classifier import MenuClassifier
import os
import sys


class MenuSpider(CrawlSpider):
    globalIdx = 2
    rules = (
        Rule(LinkExtractor(unique=True), callback='parse_item', follow=False),
    )
    name ="restaurant_menu_crawler"
    processed_urls = []

    #start_urls=['https://menupages.com']
    #start_urls=['https://menupages.com/fish-poke-bar/56-reade-st-new-york']
    #start_urls=['https://salathairestaurants.com/sala-thai-%231']
    #start_urls=['https://medium.com/youngwonks/maths-competitions-for-elementary-school-students-in-the-us-3e747bea33e2','https://www.mixerdirect.com/blogs/mixer-direct-blog/10-chemistry-blogs-you-should-read','https://blog.hubspot.com/sales/real-estate-blogs','https://www.modestmoney.com/top-finance-blogs/']
    #start_urls=['https://menupages.com/fish-poke-bar/56-reade-st-new-york','https://menupages.com/pulled-chopped-bbq-sandwiches-bowls/119-e-23rd-st-new-york','https://menupages.com/svk-sous-vide-kitchen/119-e-23rd-st-new-york','https://menupages.com/wrapido-23rd-st/171-w-23rd-st-new-york','https://menupages.com/1a-canaan-sushi/154-w-29th-st-new-york','https://menupages.com/healthy-by-sunburst/26-prince-st-new-york','https://menupages.com/1-bite-grill/119-e-60th-street-new-york','https://menupages.com/1-up-bistro/1404-madison-ave-new-york','https://menupages.com/105-deli-grill/922-amsterdam-ave-new-york','https://menupages.com/107-west/2787-broadway-ave-new-york','https://menupages.com/108-food-dried-hot-pot/2794-broadway-new-york','https://menupages.com/109-spicy-gourmet-deli/990-amsterdam-ave-new-york','https://menupages.com/10th-avenue-pizza-cafe/256-10th-ave-new-york','https://menupages.com/11-hanover-greek/11-hanover-sq-new-york','https://menupages.com/118-kitchen/1-e-118th-st-new-york','https://menupages.com/11b-express/174-ave-b-new-york','https://menupages.com/11th-street-cafe/327-w-11th-st-new-york','https://menupages.com/12-chairs-soho/56-macdougal-st-new-york','https://menupages.com/16-handles-frozen-yogurt-ice-cream-ues-1st-ave/1161-1st-ave-new-york','https://menupages.com/16-handles-frozen-yogurt-ice-cream-ues-2nd-ave/1569-2nd-ave-new-york','https://menupages.com/16-handles-frozen-yogurt-ice-cream-uws-amsterdam/325-amsterdam-ave-new-york','https://menupages.com/16-handles-frozen-yogurt-ice-cream-uws-broadway/2600-broadway-ave-new-york','https://menupages.com/164-presbyterian-deli/1081-st-nicholas-ave-new-york','https://menupages.com/1428-haight-patio-and-crepery/1428-haight-st-san-francisco','https://menupages.com/21-taste-house/1109-ocean-ave-san-francisco','https://menupages.com/21st-amendment-brewery/563-2nd-st-san-francisco','https://menupages.com/3rd-street-grill/695-3rd-st-san-francisco','https://menupages.com/6th-and-b/452-balboa-street-san-francisco','https://menupages.com/7-mission-vietnamese-chinese/150-7th-st-san-francisco','https://menupages.com/77-chinese-cuisine-hawaiian/77-battery-st-san-francisco','https://menupages.com/a-desi-cafe/1501-noriega-st-san-francisco','https://menupages.com/a-taste-of-vietnam-noodle-bar-and-grill/629-broadway-ave-san-francisco','https://menupages.com/academy-bar-kitchen/1800-fillmore-st-san-francisco','https://menupages.com/adams-grub-truck/601-mission-bay-blvd-n-san-francisco','https://menupages.com/adams-grub-truck-chug-pub/1849-lincoln-ave-san-francisco','https://menupages.com/aicha-moroccan/1303-polk-st-san-francisco','https://menupages.com/ajs-bbq-and-cafe/2275-san-jose-ave-san-francisco','https://menupages.com/akiba/3141-clement-st-san-francisco','https://menupages.com/akikos-sushi-bar/542-mason-st-ste-a-san-francisco','https://menupages.com/als-super-cafe/3286-mission-st-san-francisco','https://menupages.com/al-masri-egyptian-restaurant/4031-balboa-st-san-francisco','https://menupages.com/alamo-square-cafe/711-fillmore-st-san-francisco','https://menupages.com/albona/545-francisco-st-san-francisco','https://menupages.com/alhamra-indian-pizza-and-curry/3083-16th-st-san-francisco','https://menupages.com/ali-babas-cave/799-valencia-st-san-francisco','https://menupages.com/alimento/507-columbus-ave-san-francisco','https://menupages.com/all-star-cafe/98-9th-st-san-francisco','https://menupages.com/aloha-bbq/4935-mission-st-san-francisco','https://menupages.com/amals-deli/1416-haight-st-san-francisco','https://menupages.com/amarena/2162-larkin-st-san-francisco']
    #start_urls=['https://menupages.com/pulled-chopped-bbq-sandwiches-bowls/119-e-23rd-st-new-york']

    def __init__(self, input_urls=None, allowed_domains=None, *args, **kwargs):
        print("Spider Initialized...")
        super(MenuSpider, self).__init__(*args, **kwargs)
        self.start_urls = str(input_urls).split(',')

        if allowed_domains:
            self.allowed_domains = str(allowed_domains).split(',')
        self.classifier = kwargs.get('classifier')

    def parse_item(self, response):
        global globalIdx
        """
        1. Crawl the webpage and extract the contents.
        2. Parase and Fetch the contents
        3. Classify whether the Contents are relevant to Menu
        4.
        :param response: - response of fetch
        :return: items
        """
        print("Got Parse Item...")
        MenuSpider.processed_urls.append(response.url)
        page_data = PageData()
        pageURL = response.url
        page_data['url'] = pageURL
        page_data['link_text'] = response.meta.get('link_text', '') if response.meta else ''
        soup = BeautifulSoup(response.body, 'html.parser')

        page_body = self.retrieve_body(soup)
        page_title = self.retrieve_title(soup)
        page_data['page_body'] = page_body
        page_data['page_title'] = page_title
        links = self.retrieve_links(response, soup)

        #print(response.url)
        #print("ptitle",page_title)
        #print("pbody",page_body)
        #print(self.classifier)
        # get score of the page based upon classifier
        if self.classifier:
            score = self.classifier.score(page_data['link_text'], page_title, page_body)
        else:
            score = 0.0
        page_data['score']=score
        yield page_data
        if score <= 0:
            self.log(pageURL+"This page is not related to menus",logging.INFO)
        else:
            for link in links:
                req = Request(link, priority=int(score * 100), callback=self.parse_item)
                yield req
                #yield self.parse_location(response)
        print("_____________________________________________________________________________________")

    def retrieve_title(self, soup):
        #retrieve the title from head tag.
        head = soup.find("head")
        if head and head.find("title"):
            return head.find("title").get_text()
        else:
            return ''

    def retrieve_body(self, soup):
        #retrieve body from the HTML document.
        body = soup.find("body")
        body_text = ''
        #if not body:
            #return body_text

        for pTag in body.find_all('p'):
            #body_text += pTag.get_text() + "\n"
            body_text += pTag.get_text().rstrip()
        #print("??? Body...",body_text)
        return body_text

    def retrieve_links(self, response, soup):
        #retrieve links
        links = []
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            # Convert relative href to full uri
            if href and href.startswith("/"):
                href = response.urljoin(href)
            else:
                continue
            links.append(href)
        return links
