import scrapy, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import toolsListOut
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem
from scrapy.crawler import CrawlerProcess

class ToolsSpider(CrawlSpider):
    name ='tools'
    #allowed_domains = ['']
    #start_urls = toolsListOut
    
    print(len(toolsListOut))
    # print("URL to scrap: ")
    # print(start_urls)
    #user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    

    def start_requests(self):
        self.counter = 0
        for url in toolsListOut:
            self.counter +=1
            print(f"{self.counter} -- {url['url']}")
            req = scrapy.Request(url['url'], callback = self.parse_httpbin, meta = {'dont_retry' : True,  'download_timeout' : 10, 'id' : url['id'], 'name' : url['name'], 'dont_redirect' : False }, errback=self.errback_httpbin, dont_filter=True)
            yield req

    def parseHtmlTags(self, tagsList):
        tagsList = [item.replace('\n', "") for item in tagsList]
        tagsList = [item.strip() for item in tagsList]
        while("" in tagsList):
            tagsList.remove("")
        return tagsList

    def listToString(self, listInput):
        str1 = ""
        return (str1.join(listInput))

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
                elif link.startswith("http"):
                    externalLinks.append(link)
        

        scriptsTagsText = response.xpath('//script/text()').getall()
        lenScriptsTagsText = len(self.listToString(scriptsTagsText))

        # lenScriptsTagsText = len(response.xpath('//script/text()').getall())

        h1List = response.xpath('//h1/text()').getall()
        h2List = response.xpath('//h2/text()').getall()
        h3List = response.xpath('//h3/text()').getall()
        h4List = response.xpath('//h4/text()').getall()
        h1ListOut = self.parseHtmlTags(h1List)
        h2ListOut = self.parseHtmlTags(h2List)
        h3ListOut = self.parseHtmlTags(h3List)
        h4ListOut = self.parseHtmlTags(h4List)


        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = idTool
        toolItem ['bodyContent'] = len(response.text) - lenScriptsTagsText
        toolItem ['httpCode'] = response.status
        #toolItem ['scriptsTagsText'] = scriptsTagsText
        toolItem ['lenScriptsTagsText'] = lenScriptsTagsText
        
        toolItem ['JavaScript'] = "No"

        toolItem ['urlTool'] = url
        #toolItem ['nameTool'] = nameTool
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        toolItem ['metaDescription'] = response.xpath('//meta[@name="description"]/@content').get()

        toolItem ['h1'] = h1ListOut
        toolItem ['h2'] = h2ListOut
        toolItem ['h3'] = h3ListOut
        toolItem ['h4'] = h4ListOut

        #The download latency is measured as the time elapsed between establishing the TCP connection and receiving the HTTP headers:
        toolItem ['latency'] = latency
        
        #toolItem ['redirect_reasons'] = redirect_reasons
        #toolItem ['redirectUrls'] = redirectUrls
       
        toolItem ['numberRelativeLinks'] = len(relativeLinks)
        toolItem ['numberExternalLinks'] = len(externalLinks)
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
            toolItem ['bodyContent'] = 0
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = "HttpError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            toolItem ['httpCode'] = "DNSLookupError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "TimeoutError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)

        elif failure.check(TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "TCPTimedOutError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
            
        elif failure.check(ConnectError):
            toolItem ['idTool'] = idUrl
            #toolItem ['nameTool'] = nameTool
            toolItem ['bodyContent'] = 0
            toolItem ['httpCode'] = "ConnectError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem ['idTool'] = idUrl
            #toolItem ['nameTool'] = nameTool
            toolItem ['bodyContent'] = 0
            toolItem ['httpCode'] = "ConnectionRefusedError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            toolItem ['httpCode'] = "ResponseFailed"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ResponseNeverReceived"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)

        
    
    #print(len(start_urls))
