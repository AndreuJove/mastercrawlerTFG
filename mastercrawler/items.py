
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MastercrawlerItem(scrapy.Item):
    url = scrapy.Field()
    httpCode = scrapy.Field()
    title = scrapy.Field()
    
    idUrl = scrapy.Field()
    latency = scrapy.Field()
    
    errorMessage = scrapy.Field()
    
    redirectUrls = scrapy.Field()
    redirect_reasons = scrapy.Field()

    relativeLinks = scrapy.Field()
    externalLinks = scrapy.Field()
    numberRelativeLinks = scrapy.Field()
    numberExternalLinks = scrapy.Field()



    
    

