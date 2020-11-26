
""" 

This module starts the process of crawling along X websites and extract his corresponding HTML without JavaScript rendered. 
Furthermore extracts the statistics from the amount of websites given as input.

"""

import argparse
import os
import logging
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mastercrawler.spiders.crawlertools import ToolsSpider


def load_json(path_file):
    # Load JSON file
    with open(path_file) as file:
        return json.load(file)

def write_json(data, path):
    # Write on a json file. Input: data and path of the file.
    with open(path, 'w') as file:
        json.dump(data, file)

def main(args):
    # Open the file of list tools unique and save it in a list of dictionaries:
    websites_to_crawl = load_json(args.i_path_file)

    # Create empty manifest file
    dict_manifest = {}
    dict_manifest.setdefault("tools_ok", [])
    write_json(dict_manifest, f'{args.output_directory}/{args.filename_output}.json')

    # Create the logger:
    logging.basicConfig(
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %y %H:%M:%S',
                        filename=f'{args.output_directory}/{args.log_file_name}.log',
                        filemode='w'
                        )

    # Instance of CrawlerProcess and call the method to access the settings of the crawler in settings.py:
    process = CrawlerProcess(get_project_settings())

    # Method to crawl the spider in crawlertools.py and pass as **kwargs the following variables:
    process.crawl(ToolsSpider,
                    args=args,
                    list_unique_url=websites_to_crawl['websites_to_crawl'][:10])

    # Start the process of crawling.
    process.start()

    list_files = os.listdir(args.o_directory_htmls_no_js)

    logging.info(f"Websites INPUT: {len(websites_to_crawl['websites_to_crawl'])}")
    logging.info(f"HTMLs saved: {len(list_files)}")

if __name__ == "__main__":

    # Instance of the class ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crawler for bioinformatics tools and extracting the HTMLs without JS")

    # File with the websites to crawl:
    parser.add_argument(
                        '-i_path_file',
                        type=str,
                        metavar="",
                        default="../websites_filter/output_data/websites_to_crawl.json",
                        help="Input file from that has to contain an array of websites for crawling"
                        )

    # Output's directory name where the output files will be saved:
    parser.add_argument(
                        '-output_directory',
                        type=str,
                        metavar="",
                        default="output_data",
                        help="Name of the directory for the outputs file")

    # Output manifest name file:
    parser.add_argument(
                        '-filename_output',
                        type=str,
                        metavar="",
                        default="manifest_tools_scrapy",
                        help="Output filename. Contains 2 different keys: ['stats'] and ['tools_ok']"
                        )

    # Add the argument of the ouput file directory for HTMLs without JavaScript:
    parser.add_argument(
                        '-o_directory_htmls_no_js',
                        type=str,
                        metavar="",
                        default="htmls_no_js",
                        help="Name of the output directory for htmls_js"
                        )

    # Add the argument of output's directory name of log:
    parser.add_argument(
                        '-log_file_name',
                        type=str,
                        metavar="",
                        default="crawler",
                        help="Name of the output log file of the program"
                        )

    # ArgumentParser parses arguments through the parse_args() method. This will inspect the command line, convert each argument to the appropriate type and then invoke the appropriate action. In most cases, this means a simple Namespace object will be built up from attributes parsed out of the command line:
    args = parser.parse_args()

    # Check if the directory exists and if not exists create it:
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # Check if the directory exists and if not exists create it:
    if not os.path.isdir(args.o_directory_htmls_no_js):
        os.mkdir(args.o_directory_htmls_no_js)

    main(args)
