
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MastercrawlerItem(scrapy.Item):
    
    idTool = scrapy.Field()
    nameTool = scrapy.Field()
    urlTool = scrapy.Field()
    httpCode = scrapy.Field()
    titleUrl = scrapy.Field()
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    h3 = scrapy.Field()

    latency = scrapy.Field()
    errorMessage = scrapy.Field()

    redirectUrls = scrapy.Field()
    redirect_reasons = scrapy.Field()

    

    numberRelativeLinks = scrapy.Field()
    numberExternalLinks = scrapy.Field()
    relativeLinks = scrapy.Field()
    externalLinks = scrapy.Field()


    
    

