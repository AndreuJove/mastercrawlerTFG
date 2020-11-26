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

# Crawler class that inherets from CrawlSpider.
# Sourcecode of CrawlSpider available at: https://docs.scrapy.org/en/latest/_modules/scrapy/spiders/crawl.html#CrawlSpider

class ToolsSpider(CrawlSpider):
    name ='tools'
    def __init__(self, stats, settings, args, list_unique_url):
        self.stats = stats
        self.settings = settings
        self.args = args
        self.list_unique_url = list_unique_url
        dispatcher.connect(self.save_crawl_stats, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler, args, list_unique_url):
        # Overwrite from_crawler() for access to crawler.stats
        return cls(crawler.stats, crawler.settings, args, list_unique_url)

    
    def parse_scrapy_stats(self, dict_stats):
        # Parse scrapy to delete datetime object for JSON serializable. 
        for stat in dict_stats.items():
            b = stat[1]
            if isinstance(b, datetime.datetime):
                dict_stats[stat[0]] = b.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        return dict_stats


    def save_crawl_stats(self):
        # Save stats to a json file for posterior anaylisis.
        with open(f'{self.args.output_directory}/{self.args.filename_output}.json') as f:
            f_dict = json.load(f)
        f_dict['stats'] = self.parse_scrapy_stats(self.stats.get_stats())
        with open(f'{self.args.output_directory}/{self.args.filename_output}.json', 'w') as e:
            json.dump(f_dict, e)

    
    def start_requests(self):
        # It is called by Scrapy when the spider is opened.
        for url in self.list_unique_url:
            yield scrapy.Request(url,
            callback = self.parse_httpbin,
            meta = {
                'dont_retry' : True,
                'download_timeout' : 15,
                'first_url' : url,
                },
                errback=self.errback_httpbin,
                dont_filter=True)

    
    def create_item(self, first_url, final_url, error_name, html_no_js):
        # Create an item of scrapped fields.
        toolItem = MastercrawlerItem()
        toolItem ['first_url_tool'] = first_url
        toolItem ['final_url_tool'] = final_url
        toolItem ['error_name'] = error_name
        toolItem ['html_no_js'] = html_no_js
        return toolItem

    
    def parse_httpbin(self, response):  
        # Parse satisfactory response object and extract reliable information to create the item from scrapy.Request.
        toolItem= self.create_item(response.meta.get('first_url'), 
                                    response.url, 
                                    None, 
                                    response.text
                                    )
        yield toolItem
        
    
    def errback_httpbin(self, failure):
        # Parse non-satisfactory response object (failure) and catch the specific exception.
        url = failure.request.url
        if failure.check(HttpError):
            toolItem = self.create_item(url, url, "HttpError", None)
            yield (toolItem)
                
        elif failure.check(DNSLookupError):
            toolItem = self.create_item(url, url, "DNSLookupError", None)
            yield (toolItem)

        elif failure.check(TimeoutError):
            toolItem = self.create_item(url, url, "TimeoutError", None)
            yield (toolItem)

        elif failure.check(TCPTimedOutError):
            toolItem = self.create_item(url, url, "TCPTimedOutError", None)
            yield (toolItem)
            
        elif failure.check(ConnectError):
            toolItem = self.create_item(url, url, "ConnectError", None)
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem = self.create_item(url, url, "ConnectionRefusedError", None)
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem = self.create_item(url, url, "ResponseFailed", None)
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem = self.create_item(url, url, "ResponseNeverReceived", None)
            yield (toolItem)

        else:
            toolItem = self.create_item(url, url, "Unknown Exception", None)
            yield toolItem





    



