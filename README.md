
## Crawler description:
This crawler aims to determinate the status (HTTP Codes, Exceptions) and collect the HTMLS without JavaScript from the websites of a dataset of bioinformatic tools.

#### Input:
- Dataset of bioinformatics tools (used to get the websites of the bioinformatic tools).

#### Output:
- JSON file about the stats of the crawler (Exceptions, Time of execution, HTTP Codes, etc).
- JSON file that contains the websites without errors for posterior crawling with [Selenium] (https://github.com/AndreuJove/seleniumCrawler) for rendering JS.
- HTMLs of the websites without errors each one in a JSON file inside the directory of htmls_no_JS. The name of each one is the ID of the tool.
<br />


## Package installation:

- 1) Open terminal.
- 2) Go to the current directory where you want the cloned directory to be added using 'cd'.
- 3) Run the command: <br />
        $ git clone https://github.com/AndreuJove/mastercrawlerTFG.
- 4) Install requirements.txt: <br />
        $ pip3 install -r requirements.txt
- 5) From root directory and run the following command:<br />
        $ python3 main.py
- 6) The name of the output files and the directory to save them can be changed using the following command line (write it with the default values):<br />

        $ python3 main.py 
        i_path_file ../api_extraction/output_data/tools_unique_url.json 
        -o_directory output_data 
        -o_file_stats stats
        -o_directory_htmls_no_js htmls_no_js
        -o_file_tools_crawling_js tools_crawling_js
<br />


## Build with:
- [Scrapy](https://docs.scrapy.org/en/latest/) - Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.
- [Pandas](https://pandas.pydata.org/docs/) - is an opensource, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
- [Pydispatcher](https://grass.osgeo.org/grass79/manuals/libpython/pydispatch.html) - Multiple-producer-multiple-consumer signal-dispatching
- [Twisted](https://readthedocs.org/projects/twisted/) - Twisted is an event-driven networking engine written in Python and licensed under the open source.

<br />


## Authors

Andreu Jové

<br />


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE.MD](https://github.com/AndreuJove/mastercrawlerTFG/blob/master/LICENSE.md) file for details.