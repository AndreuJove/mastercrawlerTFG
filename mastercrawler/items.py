
import scrapy


class MastercrawlerItem(scrapy.Item):
    
    idTool = scrapy.Field()
    nameTool = scrapy.Field()
    html_without_scripts = scrapy.Field()
    len_html = scrapy.Field()

    #scriptsTagsText = scrapy.Field()
    #lenScriptsTagsText = scrapy.Field()

    HTML = scrapy.Field()
    
    first_url_tool = scrapy.Field()

    httpCode = scrapy.Field()
    titleUrl = scrapy.Field()
    metaDescription = scrapy.Field() 
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    h3 = scrapy.Field()
    h4 = scrapy.Field()
    
    #HarData = scrapy.Field()
    JavaScript = scrapy.Field()


    #latency = scrapy.Field()
    

    


    #redirectUrls = scrapy.Field()
    #redirect_reasons = scrapy.Field()


    # numberRelativeLinks = scrapy.Field()
    # numberExternalLinks = scrapy.Field()
    #relativeLinks = scrapy.Field()
    #externalLinks = scrapy.Field()


    
    

