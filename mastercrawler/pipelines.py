import json


class MastercrawlerPipeline(object):
    """    
    After an item has been scraped by a spider, it is sent to the Item Pipeline which processes it through several components that are executed sequentially.
    """

    #Access stats from item pipeline
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    #Return stats from item pipeline to the crawler.
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    #Write on a json file. Input: data and path of the file.
    def write_json(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)
    
    #Load json file and return list of dictionaries. Input: and path of the file.
    def load_json(self, path_file):
        with open(path_file) as f:
            return json.load(f)

    #Check if item has no error, and append on file for crawling js.
    def append_item_for_crawling_js(self, item, final_id):
        item_no_error = {
            'final_url_tool': item['final_url_tool'], 'idTool': final_id}
        path_final_file = '../output_data/tools_for_crawling_js.json'
        try:
            data = self.load_json(path_final_file)
            data.append(item_no_error)
            self.write_json(data, path_final_file)
        except:
            final_list = []
            final_list.append(item_no_error)
            self.write_json(final_list, path_final_file)

    #Get unique Id to create a file with this name.
    def parse_id(self, item):
        id = item['idTool']
        if type(id) == list:
            id = item['idTool'][0]
        return id

    #Recieve item. Parse item. Write item on a json file for posterior access.
    def process_item(self, item, spider):
        unique_id = self.parse_id(item)
        if item['error_name'] == None:
            self.append_item_for_crawling_js(item, unique_id)
        last_list_of_dicts = [dict({value[0]: value[1]})
                              for value in item.items()]
        unique_id = unique_id.split("/")[-1]
        path_tool = f"../htmls_no_JS/{unique_id}.json"
        self.write_json(last_list_of_dicts, path_tool)
        return item

