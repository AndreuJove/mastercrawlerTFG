import argparse
import os
import logging
import json
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mastercrawler.spiders.crawlertools import ToolsSpider


if __name__ == "__main__":
    # Instance of the class ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crawler for bioinformatics tools and extracting the HTMLs without JS")

    # Input file for crawling this package: Each tool has: ['name'], ['id'] and ['first_url_tool'] URL of the api to extract the data:
    parser.add_argument(
                        '-i_path_file',
                        type=str,
                        default="../api_extraction/output_data/metrics_api_v.json",
                        help="Input file from Api_Extractions. Each tool has: ['name'], ['id'] and ['first_url_tool']"
                        )

    # Output's directory name where the output files will be saved:
    parser.add_argument(
                        '-output_directory',
                        type=str,
                        default="output_data",
                        help="Name of the directory for the outputs file")

    # Ouput file name
    # Contains 2 different keys:
    # ['stats'] which is a dictionary of all the collected stats from the crawler.
    # ['tools_list_unique']
    parser.add_argument( 
                        '-filename_output',
                        type=str,
                        default="stats_and_tools_ok",
                        help="Output filename. Contains 2 different keys: ['stats'] and ['tools_ok"
                        )

    # Add the argument of the ouput file name for stats:
    parser.add_argument(
                        '-o_directory_htmls_no_js',
                        type=str,
                        default="htmls_no_js",
                        help="Name of the output stats file from crawler"
                        )

    #ArgumentParser parses arguments through the parse_args() method. This will inspect the command line, convert each argument to the appropriate type and then invoke the appropriate action. In most cases, this means a simple Namespace object will be built up from attributes parsed out of the command line:
    args = parser.parse_args()
    
    # Check if the directory exists and if not exists create it:
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # Check if the directory exists and if not exists create it:
    if not os.path.isdir(args.o_directory_htmls_no_js):
        os.mkdir(args.o_directory_htmls_no_js)

    # Open the file of list tools unique and save it in a list of dictionaries:
    with open(args.i_path_file, "r") as fp:
        metrics = json.load(fp) 

    #Create the logger:
    logging.basicConfig(format='%(levelname)s: %(message)s (%(asctime)s)', level=logging.INFO)

    logging.info(f"Starting the crawler of {len(metrics['tools_list_unique'])} websites")
    
    #Instance of CrawlerProcess and call the method to access the settings of the crawler in settings.py: 
    process = CrawlerProcess(get_project_settings())

    #Method to crawl the spider in crawlertools.py and pass as **kwargs the following variables:
    process.crawl(ToolsSpider, args=args, list_unique_url=metrics['tools_list_unique'][:3])

    #Start the process of crawling
    process.start()



