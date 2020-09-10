import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import tools_list_unique_url
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem
from scrapy.crawler import CrawlerProcess

class ToolsSpider(CrawlSpider):
    name ='tools'
    def start_requests(self):
        """
        Start the crawler with the list of tools with unique URL
        """
        self.counter = 0
        for url in tools_list_unique_url[:10]:
            self.counter +=1
            print(f"{self.counter} -- {url['first_url_tool']}")
            yield scrapy.Request(url['first_url_tool'],
            callback = self.parse_httpbin,
            meta = {
                'dont_retry' : True,
                'download_timeout' : 15,
                'first_url' : url['first_url_tool'],
                'id' : url['id'],
                'name' : url['name']},
                errback=self.errback_httpbin,
                dont_filter=True)
             
#Parse response object from a successfull request:
    def parse_httpbin(self, response):  
        url = response.url

        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = response.meta.get('id')
        toolItem ['nameTool'] = response.meta.get('name')

        # toolItem ['HTML'] = response.body
        toolItem ['httpCode'] = response.status   
        toolItem ['first_url_tool'] = response.meta.get('name')

        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        toolItem ['metaDescription'] = response.xpath('//meta[@name="description"]/@content').get()




        # toolItem ['latency'] = response.meta.get('download_latency')
        
        #toolItem ['redirect_reasons'] = response.meta.get('redirect_reasons')
        #toolItem ['redirectUrls'] = response.meta.get('redirect_urls')
       
        #toolItem ['numberRelativeLinks'] = len(relativeLinks)
        #toolItem ['numberExternalLinks'] = len(externalLinks)
        #toolItem ['externalLinks'] = externalLinks
        #toolItem ['relativeLinks'] = relativeLinks
        yield toolItem
        
    
    def errback_httpbin(self, failure):
        url = failure.request.url
        #print("Entered in errback_httpin: " + url)
        errbackUrls = []
        errbackUrls.append(url)
        toolItem = MastercrawlerItem()
        nameTool = failure.request.meta.get('name') 
        idUrl = failure.request.meta.get('id') 
        request = failure.request
 
        if failure.check(HttpError):
            toolItem ['html_without_scripts'] = 0
            toolItem ['idTool'] = idUrl
            #toolItem ['httpCode'] = "HttpError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['httpCode'] = "DNSLookupError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = "TimeoutError"
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)

        elif failure.check(TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = "TCPTimedOutError"
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
            
        elif failure.check(ConnectError):
            toolItem ['idTool'] = idUrl
            #toolItem ['nameTool'] = nameTool
            toolItem ['html_without_scripts'] = 0
            #toolItem ['httpCode'] = "ConnectError"
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem ['idTool'] = idUrl
            #toolItem ['nameTool'] = nameTool
            toolItem ['html_without_scripts'] = 0
            #toolItem ['httpCode'] = "ConnectionRefusedError"
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            #toolItem ['httpCode'] = "ResponseFailed"
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = "ResponseNeverReceived"
            toolItem ['first_url_tool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)

        
    
    
