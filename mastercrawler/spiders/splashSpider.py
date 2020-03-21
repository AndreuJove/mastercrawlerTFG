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
            yield SplashRequest(url = url ['url'], callback=self.parse, errback=self.errback_httpbin)

           
    def parse(self, response):
        toolItem = MastercrawlerItem()
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield toolItem



        
    def errback_httpbin(self, failure):
        url = failure.request.url
        print("Entered in errback_httpin: " + url)
        toolItem = MastercrawlerItem()
        nameTool = failure.request.meta.get('name') 
        idUrl = failure.request.meta.get('id') 
        request = failure.request
        
        if failure.check(HttpError):
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = HttpError
            toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = request.url
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = request.url
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['urlTool'] = request.url
            yield (toolItem)

        elif failure.check(ConnectError):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = ConnectError
            toolItem ['urlTool'] = request.url
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = ConnectionRefusedError
            toolItem ['urlTool'] = request.url
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            toolItem ['httpCode'] = ResponseFailed
            toolItem ['urlTool'] = request.url
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = ResponseNeverReceived
            toolItem ['urlTool'] = request.url
            yield (toolItem)