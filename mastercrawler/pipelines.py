"""
After an item has been scraped by a spider, it is sent to the Item Pipeline which processes
it through several components that are executed sequentially.
"""

import json

class MastercrawlerPipeline():

    def __init__(self, stats):
        """ Access stats from item pipeline"""
        self.stats = stats
        self.counter = 0

    @classmethod
    def from_crawler(cls, crawler):
        """ Return stats from item pipeline to the crawler."""
        return cls(crawler.stats)

    @staticmethod
    def write_json(data, path):
        """ Write on a json file. Input: data and path of the file."""
        with open(path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def load_json(path_file):
        """ Load json file and return list of dictionaries. Input: and path of the file."""
        with open(path_file) as file:
            return json.load(file)

    def append_item_for_crawling_js(self, item):
        """ Check if item has no error, and append on file his correspoding file."""
        item_no_error = {
                            'final_url': item['final_url_tool'],
                            'first_url' : item['first_url_tool'],
                            'path_file' : f"entry_{self.counter}.json"
                        }
        path_final_file = f'{self.args.output_directory}/{self.args.filename_output}.json'

        data = self.load_json(path_final_file)
        data['tools_ok'].append(item_no_error)
        self.write_json(data, path_final_file)

    def open_spider(self, spider):
        """ Access the args of the spider (ToolsSpider) and safe it in self.args """
        self.args = spider.args

    def process_item(self, item, spider):
        """ Recieve item. Parse item. Write item on a json file for posterior access."""
        if item['error_name'] is None:
            self.counter +=1
            self.append_item_for_crawling_js(item)
            path_tool = f"{self.args.o_directory_htmls_no_js}/entry_{self.counter}.json"
            tool_dict = {
                        'first_url' : item['first_url_tool'],
                        'html_no_js' : item['html_no_js']
                        }
            self.write_json(tool_dict, path_tool)
        return item

