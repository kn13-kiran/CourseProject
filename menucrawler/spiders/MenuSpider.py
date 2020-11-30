# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from focused_scrapy_crawler.items import FocusedScrapyCrawlerItem
import time
import logging
from scrapy.http import Request
from classifier import WebClassifier
from bs4 import BeautifulSoup


class MenuSpider(CrawlSpider):

    rules = (
        Rule(LinkExtractor(unique=True), callback='parse_item', follow=False),
    )

    processed_urls = []

    def __init__(self, input_urls=None, allowed_domains=None, *args, **kwargs):
        """
        Initialized crawl
        :param input_urls: comma separates list of uris
        :param allowed_domains: allowed domains
        :param args: list of args
        :param kwargs: key value args
        """
        super(MenuSpider, self).__init__(*args, **kwargs)
        self.start_urls = str(input_urls).split(',')
        if allowed_domains:
            self.allowed_domains = str(allowed_domains).split(',')
        # Initialized classifier
        self.classifier = kwargs.get('classifier')

    def parse_item(self, response):
        """
        crawling the webpage and extracts the url.
        Once the crawling is done, evaluate the page content is relevant to new house or not
        :param response: - response of fetch
        :return: items
        """
        MenuSpider.processed_urls.append(response.url)
        page_data = PageData()
        page_data['url'] = response.url
        page_data['link_text'] = response.meta.get('link_text', '') if response.meta else ''
        soup = BeautifulSoup(response.body, 'html.parser')

        page_data['body_p_tags'] = self._getBodyText(soup)
        page_data['head_title'] = self._getHeadTitle(soup)
        page_data['last_crawled'] = time.time()
        links = self._getLinks(response, soup)

        # get score of the page based upon classifier
        if self.classifier:
            score = self.classifier.score(page_data['link_text'], page_data['head_title'], page_data['body_p_tags'])
        else:
            score = 0.0

        page_data['score'] = score
        yield page_data
        if score <= 0:
            self.log("page_data={} doesn't contain Menu Page, ignore parsing ".format(page_data),logging.INFO)
        else:
            for link in links:
                req = Request(link, priority=int(score * 1000000),  # after the request is done, run parse_item to train the apprentice
                              callback=self.parse_item)
                yield req

    def _getHeadTitle(self, soup):
        """
        Get head title
        :param soup: beautiful soup instance
        :return: head title text
        """
        head = soup.find("head")
        if not head:
            return ''
        if head and head.find("title"):
            return head.find("title").get_text()
        else:
            return ''

    def _getBodyText(self, soup):
        """
        get body text
        :param soup: beautiful soup instance
        :return: all body paragraph
        """
        body = soup.find("body")
        body_text = ''
        if not body:
            return body_text
        for pTag in body.find_all('p'):
            body_text += pTag.get_text() + "\n"
        return body_text

    def _getLinks(self, response, soup):
        """
        Get anchor tags for whole page
        :param response: response object instance
        :param soup: beautiful soup instance
        :return: list of urls
        """
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
