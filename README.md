
## Crawler description:
This crawler aims to determinate the status and collect the HTMLS without JavaScript from the websites of a dataset of bioinformatic tools.

#### Input:
- Dataset of bioinformatics tools (the access to their websites).

#### Output:
- JSON file that contains the count of the most common domains in these websites.
- JSON file of the primary classification about the precedence of these websites. 
- JSON file of problematic URLs for crawling (.pdf, .gz, etc).
- JSON file of the tools 
- JSON file about the stats of the crawler (Exceptions, Time of execution, HTTP Codes, etc).
- JSON file that contains the tools and his websites without errors for posterior crawling for rendering JS.
- HTMLs of the websites without errors each one in a JSON file inside the directory of htmls_no_JS. The name of each one is the ID of the tool.


## Package installation:

- 1) Open terminal.
- 2) Go to the current directory where you want the cloned directory to be added using 'cd'.
- 3) Run the command: 
        $ git clone https://github.com/AndreuJove/mastercrawlerTFG.
- 4) Install requirements.txt:
        $ pip3 install -r requirements.txt
- 5) Move to mastercrawler/spiders and run the following command:
        $ scrapy crawl tools


## Build with:
- [Scrapy](https://docs.scrapy.org/en/latest/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Pydispatcher](https://grass.osgeo.org/grass79/manuals/libpython/pydispatch.html)
- [Twisted](https://readthedocs.org/projects/twisted/)

<br />
---

### Authors

Andreu Jové

<br />
---

### License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE.MD](https://github.com/AndreuJove/mastercrawlerTFG/blob/master/LICENSE.md) file for details.