import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from ..items import MastercrawlerItem
import urllib.parse

class ToolsSpider(CrawlSpider):
    name ='tools'
    #allowed_domains = ['']
    print("List to crawl: \n {}".format(toolUrlList))
    print(len(toolUrlList))
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
        httpCode = response.status
        url = response.url
        title = response.xpath('//title/text()').get()
        allLinks = response.xpath('//a/@href').getall()
        linksParsed = []
        for link in allLinks:
            
            if link not in linksParsed:
                if link.startswith("http"):
                    linksParsed.append(link)
                elif link.startswith("/") or link.startswith("#") or link[:1].isalpha():
                    relative_url = url + link
                    linksParsed.append(relative_url)
                else: 
                    continue
            else:
                continue     
        #or link[0].isalpha()   
        # linksParsed = []
        # for link in alllinks:
        #     if link 
        
        #linksOfthePage = response.xpath("//a[starts-with(@href, 'http')]/@href").getall()
        
        # if httpCode == 301:
        #       redirectUrls = response.request.meta['redirect_urls']
              

        toolItem = MastercrawlerItem()
        toolItem ['url'] = url
        toolItem ['httpCode'] = httpCode
        toolItem ['title'] = title
        toolItem ['links'] = linksParsed
        toolItem ['numberlinks'] = len(linksParsed)
        
        yield toolItem
        
    
    def errback_httpbin(self, failure):
        url = failure.request.url
        print("Entered in errback_httpin: " + url)
        #self.logger.error(repr(failure))
        if failure.check(HttpError):
            request = failure.request
            self.logger.error('HttpError on %s', request.url)
                  
        elif failure.check(DNSLookupError):
            request = failure.request
            toolItem = MastercrawlerItem()
            toolItem ['url'] = request.url
            toolItem ['httpCode'] = failure.getErrorMessage()
            toolItem ['title'] = "None"
            toolItem ['links'] = "None"
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
        
        
    
    