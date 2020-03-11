
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MastercrawlerItem(scrapy.Item):
    url = scrapy.Field()
    httpCode = scrapy.Field()
    title = scrapy.Field()
    #links = scrapy.Field()
    numberlinks = scrapy.Field()
    latency = scrapy.Field()
    redirectUrls = scrapy.Field()
    errorMessage = scrapy.Field()
    #latencyTime = scrapy.Field()
    idUrl = scrapy.Field()
    redirect_reasons = scrapy.Field()
    



    
    

