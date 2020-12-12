import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from menu_classifier import MenuClassifier

def main(args):
    if len(args) < 2:
        print("Missing the list of URLs that need to be checked")
        print("Usage - python main.py url1,url2,..urln ")
        print("Example - python main.py https://www.cnn.com,https://papillonrestaurant.com")
    else:
        urls = args[1]
        classifier = MenuClassifier(os.path.abspath("config.toml"))
        startCrawl(input_urls=urls, classifier=classifier)

def startCrawl(input_urls, classifier):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'menucrawler.settings')
    print("Crawling URLs %s " %input_urls )
    print("Press Ctrl+C to terminate crawling")
    truncate_file("finalresults/restaurant_menu_crawler_all_links.txt")
    truncate_file("finalresults/restaurant_menu_crawler_menu_links.txt")
    truncate_file("menucrawler/log/menucrawler.log")

    process = CrawlerProcess(get_project_settings())
    process.crawl('restaurant_menu_crawler', input_urls, classifier=classifier)
    process.start()
    print("Processing done...")

def truncate_file(filepath):
	with open(filepath, "r+") as fp:
		fp.truncate()

if __name__ == '__main__':
	main(sys.argv)
