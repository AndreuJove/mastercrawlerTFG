# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class MastercrawlerPipeline(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def write_json(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)

    def load_json(self, path_file):
        with open(path_file) as f:
            return json.load(f)

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

    def parse_id(self, item):
        id = item['idTool']
        if type(id) == list:
            id = item['idTool'][0]
        return id

    def process_item(self, item, spider):
        unique_id = self.parse_id(item)
        if item['error_name'] == None:
            self.append_item_for_crawling_js(item, unique_id)
        last_list_of_dicts = [dict({value[0]: value[1]})
                              for value in item.items()]
        unique_id = unique_id.split("/")[-1]
        print(last_list_of_dicts)
        path_tool = f"../htmls_no_JS/{unique_id}.json"
        self.write_json(last_list_of_dicts, path_tool)
        return item

