import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from menu_classifier import MenuClassifier

def main(args):
    if len(args) < 2:
        print("Usage")
    urls = args[1]
    classifier = MenuClassifier(os.path.abspath("config.toml"))
    startCrawl(input_urls=urls, classifier=classifier)

def truncate_file(filepath):
	with open(filepath, "r+") as fp:
		fp.truncate()

def startCrawl(input_urls, classifier=None):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'menucrawler.settings')
    print("starting...")
    truncate_file("finalresults/restaurant_menu_crawler_all_links.txt")
    truncate_file("finalresults/restaurant_menu_crawler_menu_links.txt")
    #truncate_file("finalresults/log/crawler.log")

    process = CrawlerProcess(get_project_settings())
    process.crawl('restaurant_menu_crawler', input_urls, classifier=classifier)
    process.start()
    print("done...")

if __name__ == '__main__':
	main(sys.argv)
