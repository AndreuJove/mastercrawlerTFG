import scrapy, json
import os
from scrapy.spiders import CrawlSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem
from scrapy import crawler
from pydispatch import dispatcher
from scrapy import signals
import datetime

#Crawler class that inherets from CrawlSpider.
#Sourcecode of CrawlSpider available at: https://docs.scrapy.org/en/latest/_modules/scrapy/spiders/crawl.html#CrawlSpider

class ToolsSpider(CrawlSpider):
    name ='tools'
    def __init__(self, stats, settings, args, list_unique_url):
        self.stats = stats
        self.settings = settings
        self.args = args
        self.list_unique_url = list_unique_url
        dispatcher.connect(self.save_crawl_stats, signals.spider_closed)

    #Overwrite from_crawler() for access to crawler.stats
    @classmethod
    def from_crawler(cls, crawler, args, list_unique_url):
        # new_args = []
        # spider = super().from_crawler(crawler, args[0], crawler.stats, crawler.settings, *args[1:], **kwargs)
        # return spider
        return cls(crawler.stats, crawler.settings, args, list_unique_url)

    #Parse scrapy to delete datetime object for JSON serializable. 
    def parse_scrapy_stats(self, dict_stats):
        list_stats = []
        for stat in dict_stats.items():
            b = stat[1]
            if isinstance(b, datetime.datetime):
                b = b.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            list_stats.append(dict({stat[0] : b}))
        return list_stats

    #Save stats to a json file for posterior anaylisis.
    def save_crawl_stats(self):
        with open(f'{self.args.output_directory_data}/{self.args.file_name_stats}.json', 'w') as e:
            json.dump(self.parse_scrapy_stats(self.stats.get_stats()), e)

    #It is called by Scrapy when the spider is opened for scraping. 
    def start_requests(self):
        for url in self.list_unique_url:
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

    #Create an item of scrapped fields.
    def create_item(self, first_url, final_url, id, name, error_name, html_no_js):
        toolItem = MastercrawlerItem()
        toolItem ['first_url_tool'] = first_url
        toolItem ['idTool'] = id
        toolItem ['nameTool'] = name
        toolItem ['final_url_tool'] = final_url
        toolItem ['error_name'] = error_name
        toolItem ['html_no_js'] = html_no_js
        return toolItem

    #Parse satisfactory response object and extract reliable information to create the item from scrapy.Request
    def parse_httpbin(self, response):  
        toolItem= self.create_item(response.meta.get('first_url'), response.url, response.meta.get('id'), response.meta.get('name'), None, response.text)
        yield toolItem
        
    #Parse non-satisfactory response object (failure) and catch the specific exception.
    def errback_httpbin(self, failure):
        url = failure.request.url
        id = failure.request.meta.get('id')
        name = failure.request.meta.get('name')
        if failure.check(HttpError):
            toolItem = self.create_item(url, url, id, name, "HttpError", None)
            yield (toolItem)
                
        elif failure.check(DNSLookupError):
            toolItem = self.create_item(url, url, id, name, "DNSLookupError", None)
            yield (toolItem)

        elif failure.check(TimeoutError):
            toolItem = self.create_item(url, url, id, name, "TimeoutError", None)
            yield (toolItem)

        elif failure.check(TCPTimedOutError):
            toolItem = self.create_item(url, url, id, name, "TCPTimedOutError", None)
            yield (toolItem)
            
        elif failure.check(ConnectError):
            toolItem = self.create_item(url, url, id, name, "ConnectError", None)
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem = self.create_item(url, url, id, name, "ConnectionRefusedError", None)
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem = self.create_item(url, url, id, name, "ResponseFailed", None)
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem = self.create_item(url, url, id, name, "ResponseNeverReceived", None)
            yield (toolItem)

        else:
            toolItem = self.create_item(url, url, id, name, "Unknown Exception", None)
            yield toolItem





    



