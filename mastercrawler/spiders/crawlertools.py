import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ToolsSpider(CrawlSpider):
    name ='tools'
    #allowed_domains = ['']
    print("List to crawl: \n {}".format(toolUrlList))
    #print(toolUrlList)
    start_urls = toolUrlList
    #handle_httpstatus_list = [404]
    #user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    
    # def __init__(self, startUrls, *args, **kwargs):
    #     # print(toolUrlList)
    #     super(ToolsSpider, self).__init__(*args, **kwargs)
    #     self.urls = startUrls

    def start_requests(self):
        #print("startrequest called")
        for url in self.start_urls:
            print("startrequest called>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            yield scrapy.Request(url, callback = self.parse_httpbin, meta = {'handle_httpstatus_all' : True, 'dont_retry' : True}, errback=self.errback_httpbin, dont_filter=True)
    
    def parse_httpbin(self, response):
        
        httpResponse = response.status
        
        # if httpResponse == 301:
        #     redirectUrls = response.request.meta['redirect_urls']
        url = response.url
        titleUrl = response.xpath('//title/text()').get()
        linksOfTheUrl = response.xpath("//a[starts-with(@href, 'http')]/@href").getall()
        
        yield  {
                "URL: " : url,
                "Http Response Code" : httpResponse,
                "Title of the Url" : titleUrl,
                "Links of the Url: " : linksOfTheUrl,
        
                        
        }
        

    def errback_httpbin(self, failure):
        url = failure.request.url
        print(url)
        #self.logger.error(repr(failure))
        if failure.check(HttpError):
            request = failure.value.failure
            self.logger.error('HttpError on %s', request.url)
                  
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
        
        
    
    