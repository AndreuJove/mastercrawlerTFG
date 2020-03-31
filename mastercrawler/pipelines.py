

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MastercrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

    def __init__(self, stats):
        self.stats = stats
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
