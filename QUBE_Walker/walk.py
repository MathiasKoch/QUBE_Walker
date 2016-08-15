from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.Carrier import CarrierSpider


def main():
	settings = get_project_settings()
	crawler = CrawlerProcess(settings)
	crawler.crawl(CarrierSpider())
	crawler.start()


if __name__ == '__main__':
	main()