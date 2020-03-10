import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from ..items import MastercrawlerItem

class ToolsSpider(CrawlSpider):
    name ='tools'
    #allowed_domains = ['']
    # print("List to crawl: \n {}".format(d['url'] for d in toolsListOut))
    # print(len(d['url'] for d in toolsListOut))
    
    start_urls = toolsListOut
    #handle_httpstatus_list = [404]
    #user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    # def __init__(self, startUrls, *args, **kwargs):
    #     # print(toolUrlList)
    #     super(ToolsSpider, self).__init__(*args, **kwargs)
    #     self.urls = startUrls

    
    def start_requests(self):
        for url in self.start_urls:
            print("<<<<<<<<<<<<<<<Startrequest called>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            yield scrapy.Request(url = url['url'], callback = self.parse_httpbin, meta = {'handle_httpstatus_all' : True, 'dont_retry' : True,  'download_timeout' : 2, 'id' : url['id'], 'dont_redirect' : False }, errback=self.errback_httpbin, dont_filter=True)

    #he download latency is measured as the time elapsed between establishing the TCP connection and receiving the HTTP headers.
    
    def parse_httpbin(self, response):
        #time = response.download_latency
        httpCode = response.status
        redirectUrls = response.meta.get('redirect_urls')
        if httpCode == 301:
            #getRedirections(response)
            toolItem = MastercrawlerItem()
            toolItem ['httpCode'] = httpCode
            toolItem ['redirectUrls'] = redirectUrls
            yield toolItem 
         
        idUrl = response.meta.get('id')  
        #redirectUrls = response.meta.get('redirectUrls')
        latency = response.meta.get('download_latency')
        url = response.url
        #title = response.xpath('//title/text()').get()
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
              
        #linksOfthePage = response.xpath("//a[starts-with(@href, 'http')]/@href").getall()
         
        toolItem = MastercrawlerItem()
        #toolItem ['latencyTime'] = response.time
        toolItem ['idUrl'] = idUrl
        toolItem ['httpCode'] = httpCode
        toolItem ['url'] = url
        toolItem ['title'] = response.xpath('//title/text()').get()
        toolItem ['links'] = linksParsed
        toolItem ['latency'] = latency
        toolItem ['redirectUrls'] = redirectUrls
        toolItem ['numberlinks'] = len(linksParsed)
        yield toolItem
        
    
    def errback_httpbin(self, failure):
        url = failure.request.url
        print("Entered in errback_httpin: " + url)
        toolItem = MastercrawlerItem()
        idUrl = failure.request.meta.get('id') 
        request = failure.request
        #self.logger.error(repr(failure))
        if failure.check(HttpError):
            toolItem ['idUrl'] = idUrl
            toolItem ['url'] = request.url
            toolItem ['httpCode'] = str(failure.type())
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem ['idUrl'] = idUrl
            toolItem ['url'] = request.url
            toolItem ['httpCode'] = str(failure.type())
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            toolItem ['idUrl'] = idUrl
            toolItem ['url'] = request.url
            toolItem ['httpCode'] = str(failure.type())
            yield (toolItem)
        
        
    
    