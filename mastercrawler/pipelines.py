import json
import sys

class MastercrawlerPipeline(object):
    """    
    After an item has been scraped by a spider, it is sent to the Item Pipeline which processes it through several components that are executed sequentially.
    """
    
    def __init__(self, stats):
        # Access stats from item pipeline
        self.stats = stats
        self.counter = 0

    @classmethod
    def from_crawler(cls, crawler):
        # Return stats from item pipeline to the crawler.
        return cls(crawler.stats)

    @staticmethod
    def write_json(data, path):
        # Write on a json file. Input: data and path of the file.
        with open(path, 'w') as f:
            json.dump(data, f)
    
    #Load json file and return list of dictionaries. Input: and path of the file.
    @staticmethod
    def load_json(path_file):
        with open(path_file) as f:
            return json.load(f)

    @staticmethod
    def process_id(tool):
        if isinstance(tool['idTool'], list):
            id = tool['idTool'][0]
        id = tool['idTool'].split("/")[-1]
        return id

    #Check if item has no error, and append on file his correspoding file.
    def append_item_for_crawling_js(self, item, final_id):
        item_no_error = {
                            'final_url': item['final_url_tool'], 
                            'id': item['idTool'], 
                            'name' : item['nameTool'],
                            'first_url' : item['first_url_tool'], 
                            'path_file' : f"{final_id}.json"
                        }
        path_final_file = f'{self.args.output_directory}/{self.args.filename_output}.json'
        try:
            data = self.load_json(path_final_file)
            data['tools_ok'].append(item_no_error)
            self.write_json(data, path_final_file)
        except:
            list_tools = []
            list_tools.append(item_no_error)
            final_dict = {"tools_ok" : list_tools}
            self.write_json(final_dict, path_final_file)

        return item_no_error
    #Access the args of the spider (ToolsSpider) and safe it in self.args
    def open_spider(self, spider):
        self.args = spider.args

    #Recieve item. Parse item. Write item on a json file for posterior access.
    def process_item(self, item, spider):
        if item['error_name'] == None:
            final_id = self.process_id(item)
            item_no_error = self.append_item_for_crawling_js(item, final_id)
            path_tool = f"{self.args.o_directory_htmls_no_js}/{final_id}.json"
            tool_dict = {
                        'id': item['idTool'], 
                        'html_no_js' : item['html_no_js']
                        }
            self.write_json(tool_dict, path_tool)
        return item

