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
    print(len(start_urls))
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    script = '''
        function main(splash, args)
            splash:on_request(function(request)
                request:set_timeout(15)
                request:enable_response_body()
            end)
            splash.private_mode_enabled = false
            
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            return {
                html = splash:html()
            }
        end
        
    '''
    
    # rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
    #         rur_tab[5]:mouse_click()
    #         assert(splash:wait(1))
    # splash:set_viewport_full()
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url['url'], callback=self.parse, meta={'dont retry': True, 'handle_httpstatus_all' : False, 'dont_redirect': True, 'id' : url['id'], 'name' : url['name'], 
                'splash' : { 
                    'args' : {
                        'lua_source': self.script
                    }, 
                        'endpoint' : 'execute', 'magic_response' : True 
                }
                }, errback=self.errback_httpbin)

    def listToString(self, listInput):
        str1 = ""
        return (str1.join(listInput))


    def parseHtmlTags(self, tagsList):
        tagsList = [item.replace('\n', "") for item in tagsList]
        tagsList = [item.strip() for item in tagsList]
        while("" in tagsList):
            tagsList.remove("")
        return tagsList

    def parse(self, response):
        idTool = response.meta.get('id')
        url = response.url
        nameTool = response.meta.get('name') 
        redirect_reasons = response.meta.get('redirect_reasons')
        redirectUrls = response.meta.get('redirect_urls')       
        latency = response.meta.get('download_latency')
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
        
        h1List = response.xpath('//h1/text()').getall()
        h2List = response.xpath('//h2/text()').getall()
        h3List = response.xpath('//h3/text()').getall()
        h4List = response.xpath('//h4/text()').getall()

        h1ListOut = self.parseHtmlTags(h1List)
        h2ListOut = self.parseHtmlTags(h2List)
        h3ListOut = self.parseHtmlTags(h3List)
        h4ListOut = self.parseHtmlTags(h4List)

        

        #Create Item:
        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = idTool
        toolItem ['bodyContent'] = len(response.text) - lenScriptsTagsText
        

        toolItem ['httpCode'] = response.status
        #toolItem ['JavaScript'] = "Yes"
        #toolItem ['scriptsTagsText'] = scriptsTagsText
        toolItem ['lenScriptsTagsText'] = lenScriptsTagsText

        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        toolItem ['urlTool'] = response.url
        toolItem ['metaDescription'] = response.xpath('//meta[@name="description"]/@content').get()
        
        # toolItem ['h1'] = h1ListOut
        # toolItem ['h2'] = h2ListOut
        # toolItem ['h3'] = h3ListOut
        # toolItem ['h4'] = h4ListOut

        toolItem ['latency'] = latency
        
        toolItem ['redirect_reasons'] = redirect_reasons
        toolItem ['redirectUrls'] = redirectUrls

        toolItem ['numberRelativeLinks'] = len(relativeLinks)
        toolItem ['numberExternalLinks'] = len(externalLinks)
        toolItem ['externalLinks'] = externalLinks
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
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = "HttpError"
            toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = url
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            print("Entered in DNSLookupError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = url
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            print("Entered in TimeoutError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['urlTool'] =  url
            yield (toolItem)

        elif failure.check(ConnectError):
            print("Entered in ConnectError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ConnectError"
            toolItem ['urlTool'] = url
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            print("Entered in ConnectionRefusedError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ConnectionRefusedError"
            toolItem ['urlTool'] = url
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            toolItem ['httpCode'] = "ResponseFailed"
            toolItem ['urlTool'] = url
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = "ResponseNeverReceived"
            toolItem ['urlTool'] = url
            yield (toolItem)