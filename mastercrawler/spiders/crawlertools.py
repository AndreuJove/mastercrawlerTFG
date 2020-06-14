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
   
    # def __init__(self, toolsListOut):
    #     super(CrawlSpider, self).__init__()
    #     self.toolsListOut = toolsListOut

    def start_requests(self):
        self.counter = 0
        for url in toolsListOut:
            self.counter +=1
            print(f"{self.counter} -- {url['url']}")
            yield scrapy.Request(url['url'],
            callback = self.parse_httpbin,
            meta = {
                'dont_retry' : True,
                'download_timeout' : 15,
                'id' : url['id'],
                'name' : url['name']},
                errback=self.errback_httpbin,
                dont_filter=True)
             
    def parseHtmlTags(self, tagsList):
        tagsList = [item.replace('\n', "") for item in tagsList]
        tagsList = [item.strip() for item in tagsList]
        while("" in tagsList):
            tagsList.remove("")
        return tagsList

    def listToString(self, listInput):
        str1 = ""
        return (str1.join(listInput))

    def parseLinks (self, allLinks, url):  
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
        return externalLinks, relativeLinks

    def parse_httpbin(self, response):  
        url = response.url
        allLinks = response.xpath('//a/@href').getall()
        externalLinks, relativeLinks = self.parseLinks(allLinks, url)
        scriptsTagsText = response.xpath('//script/text()').getall()
        lenScriptsTagsText = len(self.listToString(scriptsTagsText))

        # lenScriptsTagsText = len(response.xpath('//script/text()').getall())

        h1List = response.xpath('//h1/text()').getall()
        h2List = response.xpath('//h2/text()').getall()
        h3List = response.xpath('//h3/text()').getall()
        h4List = response.xpath('//h4/text()').getall()


        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = response.meta.get('id')
        toolItem ['html_without_scripts'] = len(response.body) - lenScriptsTagsText
        toolItem ['len_html'] = len(response.body)

        toolItem ['HTML'] = response.body
        toolItem ['httpCode'] = response.status
        
        #toolItem ['scriptsTagsText'] = scriptsTagsText
        #toolItem ['lenScriptsTagsText'] = lenScriptsTagsText
        
        toolItem ['JavaScript'] = "No"

        toolItem ['urlTool'] = url
        toolItem ['nameTool'] = response.meta.get('name')
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        toolItem ['metaDescription'] = response.xpath('//meta[@name="description"]/@content').get()

        toolItem ['h1'] = self.parseHtmlTags(h1List)
        toolItem ['h2'] = self.parseHtmlTags(h2List)
        toolItem ['h3'] = self.parseHtmlTags(h3List)
        toolItem ['h4'] = self.parseHtmlTags(h4List)

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
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['httpCode'] = "DNSLookupError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = "TimeoutError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)

        elif failure.check(TCPTimedOutError):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = "TCPTimedOutError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
            
        elif failure.check(ConnectError):
            toolItem ['idTool'] = idUrl
            #toolItem ['nameTool'] = nameTool
            toolItem ['html_without_scripts'] = 0
            #toolItem ['httpCode'] = "ConnectError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No"
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem ['idTool'] = idUrl
            #toolItem ['nameTool'] = nameTool
            toolItem ['html_without_scripts'] = 0
            #toolItem ['httpCode'] = "ConnectionRefusedError"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            #toolItem ['httpCode'] = "ResponseFailed"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['html_without_scripts'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = "ResponseNeverReceived"
            toolItem ['urlTool'] = request.url
            toolItem ['JavaScript'] = "No" 
            yield (toolItem)

        
    
    
