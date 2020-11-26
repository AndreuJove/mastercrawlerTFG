import scrapy

class MastercrawlerItem(scrapy.Item):
    """
    Fields of the item of the extracted information of the spider (crawlertools.py):
    """
    first_url_tool = scrapy.Field()
    final_url_tool = scrapy.Field()
    error_name = scrapy.Field()
    html_no_js = scrapy.Field()

    def __repr__(self):
        # Only print out first_url_tool after exiting the Pipeline
        return repr(f"Scraped website: {self['first_url_tool']}")
