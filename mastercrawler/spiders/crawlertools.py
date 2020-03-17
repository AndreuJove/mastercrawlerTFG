import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem



class ToolsSpider(CrawlSpider):
    name ='tools'
    #allowed_domains = ['']
    start_urls = toolsListOut
    print("number of URL: ") 
    print(len(start_urls))
    print("URL to scrap: ")
    print(start_urls)
    #user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    # def __init__(self, startUrls, *args, **kwargs):
    #     # print(toolUrlList)
    #     super(ToolsSpider, self).__init__(*args, **kwargs)
    #     self.urls = startUrls

    def start_requests(self):
        for url in self.start_urls:
            req = scrapy.Request(url = url['url'], callback = self.parse_httpbin, meta = {'handle_httpstatus_all' : False, 'dont_retry' : True,  'download_timeout' : 5, 'id' : url['id'], 'name' : url['name'], 'dont_redirect' : False }, errback=self.errback_httpbin, dont_filter=True)
            yield req

    
    
    def parse_httpbin(self, response):
        
        idTool = response.meta.get('id')
        nameTool = response.meta.get('name') 
        redirectUrls = response.meta.get('redirect_urls')
        redirect_reasons = response.meta.get('redirect_reasons')         
        latency = response.meta.get('download_latency')
        url = response.url
        allLinks = response.xpath('//a/@href').getall()

        externalLinks = []
        relativeLinks = []
        for link in allLinks:
                if url in link:
                    relativeLinks.append(link)
                elif link.startswith("/") or link.startswith("#") or link[:1].isalpha() or link.startswith("./") or link.startswith("../"):
                    relative_url = url + link
                    relativeLinks.append(relative_url)
                else:
                    externalLinks.append(link)
        
        
        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = idTool
        toolItem ['httpCode'] = response.status
        toolItem ['url'] = url
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        #The download latency is measured as the time elapsed between establishing the TCP connection and receiving the HTTP headers:
        toolItem ['latency'] = latency
        

        toolItem ['redirect_reasons'] = redirect_reasons
        toolItem ['redirectUrls'] = redirectUrls
        
       
        toolItem ['numberRelativeLinks'] = len(relativeLinks)
        toolItem ['numberExternalLinks'] = len(externalLinks)
        toolItem ['externalLinks'] = externalLinks
        toolItem ['relativeLinks'] = relativeLinks

        yield toolItem
        
    
    def errback_httpbin(self, failure):
        url = failure.request.url
        print("Entered in errback_httpin: " + url)
        toolItem = MastercrawlerItem()
        idUrl = failure.request.meta.get('id') 
        request = failure.request
        
        if failure.check(HttpError):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)

        elif failure.check(ConnectError):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idUrl'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['url'] = request.url
            yield (toolItem)

        

    
