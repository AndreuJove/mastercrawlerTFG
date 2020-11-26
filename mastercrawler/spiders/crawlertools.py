import json
import datetime
from scrapy import signals, Request
from pydispatch import dispatcher
from scrapy.spiders import CrawlSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from twisted.internet.error import TimeoutError,TCPTimedOutError,DNSLookupError,ConnectError,ConnectionRefusedError
from ..items import MastercrawlerItem

# Sourcecode CrawlSpider:
# https://docs.scrapy.org/en/latest/_modules/scrapy/spiders/crawl.html#CrawlSpider

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

    @staticmethod
    def parse_scrapy_stats(dict_stats):
        # Parse scrapy to delete datetime object for JSON serializable.
        for stat in dict_stats.items():
            key = stat[1]
            if isinstance(key, datetime.datetime):
                dict_stats[stat[0]] = key.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        return dict_stats

    def save_crawl_stats(self):
        # Save stats to a json file for posterior anaylisis.
        with open(f'{self.args.output_directory}/{self.args.filename_output}.json') as file:
            f_dict = json.load(file)
        f_dict['stats'] = self.parse_scrapy_stats(self.stats.get_stats())
        with open(f'{self.args.output_directory}/{self.args.filename_output}.json', 'w') as file:
            json.dump(f_dict, file)

    def start_requests(self):
        # It is called by Scrapy when the spider is opened.
        for url in self.list_unique_url:
            yield Request(url,
            callback = self.parse_httpbin,
            meta = {
                'dont_retry' : True,
                'download_timeout' : 15,
                'first_url' : url,
                },
                errback=self.errback_httpbin,
                dont_filter=True)

    @staticmethod
    def create_item(first_url, final_url, error_name, html_no_js):
        # Create an item of scrapped fields.
        tool_item = MastercrawlerItem()
        tool_item ['first_url_tool'] = first_url
        tool_item ['final_url_tool'] = final_url
        tool_item ['error_name'] = error_name
        tool_item ['html_no_js'] = html_no_js
        return tool_item

    def parse_httpbin(self, response):
        # Parse satisfactory response object and extract reliable data.
        tool_item= self.create_item(response.meta.get('first_url'),
                                    response.url,
                                    None,
                                    response.text
                                    )
        yield tool_item

    def errback_httpbin(self, failure):
        # Parse non-satisfactory response object (failure) and catch the specific exception.
        url = failure.request.url
        if failure.check(HttpError):
            yield self.create_item(url, url, "HttpError", None)

        elif failure.check(DNSLookupError):
            yield self.create_item(url, url, "DNSLookupError", None)

        elif failure.check(TimeoutError):
            yield self.create_item(url, url, "TimeoutError", None)

        elif failure.check(TCPTimedOutError):
            yield self.create_item(url, url, "TCPTimedOutError", None)

        elif failure.check(ConnectError):
            yield self.create_item(url, url, "ConnectError", None)

        elif failure.check(ConnectionRefusedError):
            yield self.create_item(url, url, "ConnectionRefusedError", None)

        elif failure.check(ResponseFailed):
            yield self.create_item(url, url, "ResponseFailed", None)

        elif failure.check(ResponseNeverReceived):
            yield self.create_item(url, url, "ResponseNeverReceived", None)

        else:
            yield self.create_item(url, url, "Unknown Exception", None)
