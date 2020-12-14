Restaurant Menu Crawler & Classifier
   A restaurant review company would like to provide recommendation on menu items across the world. To accomplish this goal, the first stage
   of the pipeline is to identify the URLs that relevant (i.e. find the URLs that contain menu information). This project focuses on the first stage

Components

  There are two major components of this project:

  Menu classifier - which uses anchor text, page title head>title, and body>p data to classify relevance of the page. This uses NaiveBayes classification and provides score either 0 or 1.

  Menu Spider - Web crawler that downloads, parses and extract the data from the links.

  Training data set for classifier -  I've manually created, curated and labelled menu data from menupages.com
    dataset/sample/*menu*.txt - contains menu data from different types of restaurants in different cities.
    dataset/sample/*other*.txt - contains non menu relevant data.

main.py:
  The driver code that triggers the crawling process. This component takes target URLs (URL that needs to be checked for Menu information) as an input. First, MenuClassifer is initialized using the training dataset, creates indexes and inverted indexes using MeTA. On target urls, driver code starts crawling using Scrapy engine. Scrapy Engine has a call back mechanism that calls two main components Menu Spider and Pipelines for every page that is downloaded.

MenuSpider:  
  Responsible for extracting, parsing page content and holds them in the plain text fields. This plain content is passed to the MenuClassifier and score is calculated. Based on the score, further processing of the links with in that page is determined. If the score is <=0 further parsing of the links is abandoned. Crawling ends when all the links are exhaused or when the score reaches 0.

Pipelines:
   DuplicateLinkRemover: Tracks already processed URls and removes circular links so that they don't get processed again.
   PageDataOutput : Stores the pageURL, scores to finalresults directory.

Project Dependencies
  This projects uses some third party components, you have to install these components first to run this project

Dependencies
   conda - to create python 3.5 virtual environment
   python 3.5+
   scrapy 2.3.0
   metapy
   Beautiful Soup version 4+

Install scrapy
     Crawler depends scrapy. Before running this project, install scrapy using following commands.
     pip install scrapy
Install metapy
    We are using metapy---Python bindings for MeTA. Install metapy using the following commands.
    pip install metapy
Install Beautiful Soup
  pip install beautifulsoup4


Running the project
    There is main.py file which needs to be invoked by passing target_urls (comma separated urls).
    python main.py url1,url2,...,urln
For example -
  python main.py https://papillonrestaurant.com,http://www.cnn.com

This command will generate output to finalresults folder.
  restaurant_menu_crawler_all_links.txt - holds all the urls that were crawled.
  restaurant_menu_crawler_menu_links.txt - holds the urls that contain menu informaiton.

menucrawler/log -> contains log file.

How to stop crawling
  This project will keep crawling until resources is exhausted or no more relevant url to crawl.If you want to stop crawling immediately then press [ctrl^c] which unsafely stop crawler immediately.

Future work
  Improving Sample Data -  I could add additional data to include different types of cuisines.
  Improving Classification - Current classification is binary , it can be further improved to include type of cuisine.
