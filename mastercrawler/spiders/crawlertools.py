import scrapy, json
from scrapy.spiders import CrawlSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError, ConnectError, ConnectionRefusedError
from ..items import MastercrawlerItem
from scrapy import crawler
from pydispatch import dispatcher
from scrapy import signals
import datetime

relative_path = "../input_data/tools_list_unique_url.json"

with open(relative_path, "r") as fp:
    list_unique_url = json.load(fp)   

class ToolsSpider(CrawlSpider):
    name ='tools'
    def __init__(self, stats, settings):
        self.stats = stats
        dispatcher.connect(self.save_crawl_stats, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        """
        Overwrite from_crawler() for access to crawler.stats
        """
        return cls(crawler.stats,crawler.settings)

    def parse_scrapy_stats(self, dict_stats):
        """
        Parse scrapy to delete datetime object for JSON serializable. 
        """
        list_stats = []
        for stat in dict_stats.items():
            b = stat[1]
            if isinstance(b, datetime.datetime):
                b = b.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            list_stats.append(dict({stat[0] : b}))
        return list_stats

    def save_crawl_stats(self):
        """
        Save stats to a json file for posterior anaylisis.
        """
        with open('../output_data/stats.json', 'w') as e:
            json.dump(self.parse_scrapy_stats(self.stats.get_stats()), e)

    def start_requests(self):
        """
        Start the crawler with the list of unique URL:
        """
        for url in list_unique_url[:10]:
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

    def create_item(self, first_url, final_url, id, name, error_name):
        toolItem = MastercrawlerItem()
        toolItem ['first_url_tool'] = first_url
        toolItem ['idTool'] = id
        toolItem ['nameTool'] = name
        toolItem ['final_url_tool'] = final_url
        toolItem ['JavaScript'] = "No"
        toolItem ['error_name'] = error_name
        return toolItem

    def parse_httpbin(self, response):  
        """
        Parse satisfactory response object and extract reliable information to create the item from scrapy.Request
        """
        toolItem= self.create_item(response.meta.get('first_url'), response.url, response.meta.get('id'), response.meta.get('name'), None)
        yield toolItem
        
    def errback_httpbin(self, failure):
        """
        Parse non-satisfactory response object (failure) and catch the specific exception
        """
        url = failure.request.url
        id = failure.request.meta.get('id')
        name = failure.request.meta.get('name')
        print("Entered in errback_httpin ----> " + url)
        if failure.check(HttpError):
            toolItem = self.create_item(url, url, id, name, "HttpError")
            yield (toolItem)
                  
        elif failure.check(DNSLookupError):
            toolItem = self.create_item(url, url, id, name, "DNSLookupError")
            yield (toolItem)
   
        elif failure.check(TimeoutError):
            toolItem = self.create_item(url, url, id, name, "TimeoutError")
            yield (toolItem)

        elif failure.check(TCPTimedOutError):
            toolItem = self.create_item(url, url, id, name, "TCPTimedOutError")
            yield (toolItem)
            
        elif failure.check(ConnectError):
            toolItem = self.create_item(url, url, id, name, "ConnectError")
            yield (toolItem)
        
        elif failure.check(ConnectionRefusedError):
            toolItem = self.create_item(url, url, id, name, "ConnectionRefusedError")
            yield (toolItem)
        
        elif failure.check(ResponseFailed):
            toolItem = self.create_item(url, url, id, name, "ResponseFailed")
            yield (toolItem)

        elif failure.check(ResponseNeverReceived):
            toolItem = self.create_item(url, url, id, name, "ResponseNeverReceived")
            yield (toolItem)

        else:
            toolItem = self.create_item(url, url, id, name, "Unknown Exception")
            yield toolItem
