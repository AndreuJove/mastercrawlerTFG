
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MastercrawlerItem(scrapy.Item):
    
    idUrl = scrapy.Field()
    url = scrapy.Field()
    httpCode = scrapy.Field()
    title = scrapy.Field()
    
    latency = scrapy.Field()
    errorMessage = scrapy.Field()
    
    redirectUrls = scrapy.Field()
    redirect_reasons = scrapy.Field()

    
    numberRelativeLinks = scrapy.Field()
    numberExternalLinks = scrapy.Field()
    relativeLinks = scrapy.Field()
    externalLinks = scrapy.Field()


    
    

