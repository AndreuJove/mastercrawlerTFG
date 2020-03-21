import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem
from scrapy_splash import SplashRequest


class SplashspiderSpider(CrawlSpider):
    name = 'splashSpider'
    #allowed_domains = ['example.com']
    start_urls = toolsListOut
    print(toolsListOut)
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url = url ['url'], callback=self.parse)

           
    def parse(self, response):
        toolItem = MastercrawlerItem()
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield toolItem
