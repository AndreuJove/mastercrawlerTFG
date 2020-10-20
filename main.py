import argparse
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mastercrawler.spiders.crawlertools import ToolsSpider
import json


if __name__ == "__main__":
    # Instance of the class ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crawler for bioinformatics tools with")

    # Input file for crawling this package: Each tool has: ['name'], ['id'] and ['first_url_tool'] URL of the api to extract the data:
    parser.add_argument('-i_path_file', '--path_list_tools_unique_url', type=str, 
                    default="../api_extraction/output_data/tools_unique_url.json",
                    help="File of tools unique url. Each tool has: ['name'], ['id'] and ['first_url_tool']")

    # Output's directory name where the output files will be saved:
    parser.add_argument('-o_directory', '--output_directory_data', type=str,
                    default="output_data", help="Name of the directory for the outputs files")

    # Ouput file name for stats:
    parser.add_argument('-o_file_stats', '--file_name_stats', type=str,
                    default="stats", help="Name of the output stats file from crawler")

    # Add the argument of the ouput file name for stats:
    parser.add_argument('-o_directory_htmls_no_js', '--output_directory_htmls', type=str,
                    default="htmls_no_js", help="Name of the output stats file from crawler")

    # Add the argument of the ouput file name for stats:
    parser.add_argument('-o_file_tools_crawling_js', '--tools_file_crawling_js', type=str,
                    default="tools_crawling_js", help="Name of the output file of tools for crawling JavaScript")

    #ArgumentParser parses arguments through the parse_args() method. This will inspect the command line, convert each argument to the appropriate type and then invoke the appropriate action. In most cases, this means a simple Namespace object will be built up from attributes parsed out of the command line:
    args = parser.parse_args()

    # Check if the directory exists and if not exists create it:
    if not os.path.isdir(args.output_directory_data):
        os.mkdir(args.output_directory_data)

    # Check if the directory exists and if not exists create it:
    if not os.path.isdir(args.output_directory_htmls):
        os.mkdir(args.output_directory_htmls)

    # Open the file of list tools unique and save it in a list of dictionaries:
    with open(args.path_list_tools_unique_url, "r") as fp:
        list_unique_url = json.load(fp) 

    #Instance of CrawlerProcess and call the method to access the settings of the crawler in settings.py: 
    process = CrawlerProcess(get_project_settings())

    #Method to crawl the spider in crawlertools.py and pass as **kwargs the following variables:
    process.crawl(ToolsSpider, args=args, list_unique_url=list_unique_url)

    #Start the process of crawling
    process.start()



