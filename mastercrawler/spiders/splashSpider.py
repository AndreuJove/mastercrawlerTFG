import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mastercrawler.spiders.jsonextraction import toolsListOut
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem
from scrapy_splash import SplashRequest

class SplashspiderSpider(CrawlSpider):
    name = 'splashSpider'
    
    # def __init__(self, toolsListOut):
    #     super(SplashspiderSpider, self).__init__()
    #     self.toolsListOut = toolsListOut

    script = '''
            function main(splash, args)
                assert(splash:go(args.url))
                assert(splash:wait(2))
                return {
                    html = splash:html(),
                    har = splash:har()
                }
                end
    '''

    # script = '''
    #     function main(splash, args)
    #         splash:on_request(function(request)
    #             request:set_timeout(20)
    #             request:enable_response_body()
    #             splash.private_mode_enabled = false
    #         end)    
    #         splash:go(args.url)
    #         assert(splash:wait(5))
    #         return {
    #             html = splash:html(),
    #         }
    #     end
    # '''

    def start_requests(self):
        self.counter = 0
        for url in toolsListOut:
            self.counter +=1
            print(f"{self.counter} -- {url['url']}")
            yield scrapy.Request(url = url['url'], callback=self.parse_httpbin, 
            errback=self.errback_httpbin, dont_filter=True,
            meta={
            'dont_retry': False, 
            'handle_httpstatus_all' : False, 
            'id' : url['id'], 
            'name' : url['name'], 
                'splash' : { 
                    'args' : {                        
                        'lua_source': self.script,
                        'html' : 1,
                        'har' : 1
                    }, 
                        'endpoint' : 'execute', 
                        'http_method' : 'GET',
                        'handle_httpstatus_all': True,
                        'magic_response' : True 
                }
                }) 

    def listToString(self, listInput):
        str1 = ""
        return (str1.join(listInput))

    def parseHtmlTags(self, tagsList):
        tagsList = [item.replace('\n', "") for item in tagsList]
        tagsList = [item.strip() for item in tagsList]
        while("" in tagsList):
            tagsList.remove("")
        return tagsList

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
        externalLinks, relativelinks = self.parseLinks(allLinks, url)
        scriptsTagsText = response.xpath('//script/text()').getall()
        lenScriptsTagsText = len(self.listToString(scriptsTagsText))
        
        h1List = response.xpath('//h1/text()').getall()
        h2List = response.xpath('//h2/text()').getall()
        h3List = response.xpath('//h3/text()').getall()
        h4List = response.xpath('//h4/text()').getall()



        #--------------------------------------------------------------------------------------------------
        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = response.meta.get('id')
        toolItem ['nameTool'] = response.meta.get('name')   
        toolItem ['html_without_scripts'] = len(response.body) - lenScriptsTagsText
        toolItem ['len_html'] = len(response.body)


        toolItem ['HTML'] = response.body
        toolItem ['httpCode'] = response.status


        #toolItem ['HarData'] = response.data['har']
        
        #toolItem ['scriptsTagsText'] = scriptsTagsText
        #toolItem ['len_scriptsTagsText'] = lenScriptsTagsText

        toolItem ['JavaScript'] = "Yes"

        toolItem ['urlTool'] = response.url
        
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        toolItem ['metaDescription'] = response.xpath('//meta[@name="description"]/@content').get()
        
        toolItem ['h1'] = self.parseHtmlTags(h1List)
        toolItem ['h2'] = self.parseHtmlTags(h2List)
        toolItem ['h3'] = self.parseHtmlTags(h3List)
        toolItem ['h4'] = self.parseHtmlTags(h4List)

        #The download latency is measured as the time elapsed between establishing the TCP connection and receiving the HTTP headers:
        #toolItem ['latency'] = response.meta.get('download_latency')
        
        #toolItem ['redirect_reasons'] = response.meta.get('redirect_reasons')
        #toolItem ['redirectUrls'] = response.meta.get('redirect_urls') 

        #toolItem ['numberRelativeLinks'] = len(relativeLinks)
        #toolItem ['numberExternalLinks'] = len(externalLinks)
        #toolItem ['externalLinks'] = externalLinks
        #toolItem ['relativeLinks'] = relativeLinks
        yield toolItem

    
    def errback_httpbin(self, failure):
        url = failure.request._original_url
        print("Entered in errback_httpin: " + url)
        toolItem = MastercrawlerItem()
        nameTool = failure.request.meta.get('name') 
        idUrl = failure.request.meta.get('id') 
        
        
        if failure.check(HttpError):
            print("Entered in HttpError: " + url)
            toolItem ['bodyContent'] = 0
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = "HttpError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = url
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            print("Entered in DNSLookupError: " + url)
            toolItem ['bodyContent'] = 0
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = "DNSLookupError"
            #toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = url
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            print("Entered in TimeoutError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['urlTool'] =  url
            yield (toolItem)

        elif failure.check(ConnectError):
            print("Entered in ConnectError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ConnectError"
            toolItem ['urlTool'] = url
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            print("Entered in ConnectionRefusedError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ConnectionRefusedError"
            toolItem ['urlTool'] = url
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            toolItem ['httpCode'] = "ResponseFailed"
            toolItem ['urlTool'] = url
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['bodyContent'] = 0
            #toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ResponseNeverReceived"
            toolItem ['urlTool'] = url
            yield (toolItem)