import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import *
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem


#Nou canvi pel git
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

    #Trying new n.
    def start_requests(self):
        for url in self.start_urls:
            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<Startrequest called>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            req = scrapy.Request(url = url['url'], callback = self.parse_httpbin, meta = {'handle_httpstatus_all' : False, 'dont_retry' : True,  'download_timeout' : 5, 'id' : url['id'], 'dont_redirect' : False }, errback=self.errback_httpbin, dont_filter=True)
            yield req

    #The download latency is measured as the time elapsed between establishing the TCP connection and receiving the HTTP headers.
    
    def parse_httpbin(self, response):
        
        httpCode = response.status
        redirectUrls = response.meta.get('redirect_urls')
        redirect_reasons = response.meta.get('redirect_reasons')
        # if response.status >= 300 and response.status < 400:
        #     location = to_native_str(response.headers['location'].decode('latin1'))
        #     request = response.request
        #     redirected_url = urljoin(request.url, location)
            
        #     if response.status in (301, 307) or request.method == 'HEAD':
        #         redirected = request.replace(url=redirected_url)
        #         yield redirected
        #     else:
        #         redirected = request.replace(url=redirected_url, method='GET', body='')
        #         redirected.headers.pop('Content-Type', None)
        #         redirected.headers.pop('Content-Length', None)
        #         yield redirected
            #getRedirections(response)
            # toolItem = MastercrawlerItem()
            # toolItem ['httpCode'] = httpCode
            # toolItem ['redirectUrls'] = redirectUrls
            # yield toolItem 
         
        idUrl = response.meta.get('id')  
        #redirectUrls = response.meta.get('redirectUrls')
        latency = response.meta.get('download_latency')
        url = response.url
        
        allLinks = response.xpath('//a/@href').getall()
        
        linksParsed = []
        for link in allLinks:
            if link not in linksParsed:
                if link.startswith("http"):
                    linksParsed.append(link)
                elif link.startswith("/") or link.startswith("#") or link[:1].isalpha() or link.startswith("./") or link.startswith("../"):
                    relative_url = url + link
                    linksParsed.append(relative_url)
                else: 
                    continue
              
        #linksOfthePage = response.xpath("//a[starts-with(@href, 'http')]/@href").getall()
        
        toolItem = MastercrawlerItem()
        toolItem ['idUrl'] = idUrl
        toolItem ['httpCode'] = httpCode
        toolItem ['url'] = url
        toolItem ['redirect_reasons'] = redirect_reasons
        toolItem ['title'] = response.xpath('//title/text()').get()
        #toolItem ['links'] = linksParsed
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

        

    
