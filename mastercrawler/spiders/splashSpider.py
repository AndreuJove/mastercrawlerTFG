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
                request:set_timeout(10)
                request:enable_response_body()

            end)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(0.5))
            return{
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
            yield SplashRequest(url = url['url'], callback=self.parse, errback=self.errback_httpbin, endpoint='execute', magic_response= True, args={'lua_source': self.script}, meta={'dont retry': True, 'id' : url['id'], 'name' : url['name']})
           
    def parse(self, response):
        
        idTool = response.meta.get('id')
        url = response.url
        redirect_reasons = response.meta.get('redirect_reasons')
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
        
        
        
        toolItem = MastercrawlerItem()
        toolItem ['idTool'] = idTool
        toolItem ['titleUrl'] = response.xpath('//title/text()').get()
        toolItem ['urlTool'] = response.url
        toolItem ['bodyContent'] = len(response.text)
        toolItem ['responseBody'] = len(response.body)
        toolItem ['httpCode'] = response.status
        toolItem ['redirect_reasons'] = redirect_reasons
        toolItem ['numberRelativeLinks'] = len(relativeLinks)
        toolItem ['numberExternalLinks'] = len(externalLinks)
        
        yield toolItem

    
    def errback_httpbin(self, failure):
        url = failure.request.url
        print("Entered in errback_httpin: " + url)
        toolItem = MastercrawlerItem()
        nameTool = failure.request.meta.get('name') 
        idUrl = failure.request.meta.get('id') 
        request = failure.request
        
        if failure.check(HttpError):
            print("Entered in HttpError: " + url)
            toolItem ['idTool'] = idUrl
            #toolItem ['httpCode'] = HttpError
            toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = url
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            print("Entered in DNSLookupError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['nameTool'] = nameTool
            toolItem ['urlTool'] = failure.url
            yield (toolItem)
            #self.logger.error('DNSLookupError on %s', request.url)
            
        elif failure.check(TimeoutError, TCPTimedOutError):
            print("Entered in TimeoutError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = str(failure.type())
            toolItem ['urlTool'] = failure.url
            yield (toolItem)

        elif failure.check(ConnectError):
            print("Entered in ConnectError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = ConnectError
            toolItem ['urlTool'] = request.url
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            print("Entered in ConnectionRefusedError: " + url)
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = ConnectionRefusedError
            toolItem ['urlTool'] = request.url
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            #toolItem ['httpCode'] = str(failure.type())
            #TypeError: __init__() missing 1 required positional argument: 'reasons'
            toolItem ['httpCode'] = ResponseFailed
            toolItem ['urlTool'] = failure.url
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem ['idTool'] = idUrl
            toolItem ['nameTool'] = nameTool
            toolItem ['httpCode'] = ResponseNeverReceived
            toolItem ['urlTool'] = failure.url
            yield (toolItem)