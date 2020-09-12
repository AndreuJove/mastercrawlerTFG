
import scrapy


class MastercrawlerItem(scrapy.Item):
    """
    Fields of the item for the extracted information of the crawler:
    """
    first_url_tool = scrapy.Field()
    idTool = scrapy.Field()
    nameTool = scrapy.Field()
    final_url_tool = scrapy.Field()
    error_name = scrapy.Field()
    html_no_js = scrapy.Field()




    
    

