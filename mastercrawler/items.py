
import scrapy


class MastercrawlerItem(scrapy.Item):
    
    idTool = scrapy.Field()
<<<<<<< HEAD
=======
    bodyContent = scrapy.Field()

    scriptsTagsText = scrapy.Field()
    lenScriptsTagsText = scrapy.Field()

>>>>>>> f6cf7f4338a8e0d7c1536b18f180d57a72875c96
    nameTool = scrapy.Field()
    html_without_scripts = scrapy.Field()
    len_html = scrapy.Field()

    #scriptsTagsText = scrapy.Field()
    #lenScriptsTagsText = scrapy.Field()

    HTML = scrapy.Field()
    
    urlTool = scrapy.Field()

    httpCode = scrapy.Field()
    titleUrl = scrapy.Field()
    metaDescription = scrapy.Field() 
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    h3 = scrapy.Field()
    h4 = scrapy.Field()
    
    #HarData = scrapy.Field()
    JavaScript = scrapy.Field()


<<<<<<< HEAD
    #latency = scrapy.Field()
    
=======
    

    latency = scrapy.Field()
    errorMessage = scrapy.Field()
>>>>>>> f6cf7f4338a8e0d7c1536b18f180d57a72875c96

    #redirectUrls = scrapy.Field()
    #redirect_reasons = scrapy.Field()


    # numberRelativeLinks = scrapy.Field()
    # numberExternalLinks = scrapy.Field()
    #relativeLinks = scrapy.Field()
    #externalLinks = scrapy.Field()


    
    

