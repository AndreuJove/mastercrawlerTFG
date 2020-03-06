# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MastercrawlerItem(scrapy.Item):
    url = scrapy.Field()
    httpCode = scrapy.Field()
    title = scrapy.Field()
    links = scrapy.Field()
    numberlinks = scrapy.Field()
    
    



    
    

