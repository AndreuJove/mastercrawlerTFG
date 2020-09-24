

SOFTWARE PACKAGE FOR SCRAPING WEBSITES AND CATCH THE ERRORS OF A DATASET




Author: Andreu Jové







INSTALLATION OF THIS PACKAGE:

========================================================================

1) Open terminal.

2) Go to the current directory where you want the cloned directory to be added using 'cd'.

3) Run the command: $git clone https://github.com/AndreuJove/mastercrawlerTFG

4) Install requirements.txt if it's possible in a virtual environment. 

5) Move to mastercrawler/input_data and run the following command: 
    $ wget "https://dev-openebench.bsc.es/monitor/rest/edam/aggregate?projection=description&projection=web&name=&label=null" -O final_tools_v_api.json

6) Move to mastercrawler/spiders and run the following command:
    $ scrapy crawl tools
    
========================================================================




## DESCRITION OF THE CRAWLER:
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


## Installation of this package:

- 1) Open terminal.
- 2) Go to the current directory where you want the cloned directory to be added using 'cd'.
- 3) Run the command: 
        $ git clone https://github.com/AndreuJove/mastercrawlerTFG.
- 4) Install requirements.txt:
        $ pip3 install -r requirements.txt
- 5) Move to mastercrawler/spiders and run the following command:
        $ scrapy crawl tools


### Build with:
- [Scrapy](https://docs.scrapy.org/en/latest/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Pydispatcher](https://grass.osgeo.org/grass79/manuals/libpython/pydispatch.html)
- [Twisted](https://readthedocs.org/projects/twisted/)

<br />

### Languages and Tools:

[<img align="left" alt="Python" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/visual-studio-code/visual-studio-code.png" />][webdevplaylist]
[<img align="left" alt="HTML5" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/html/html.png" />][webdevplaylist]
[<img align="left" alt="CSS3" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/css/css.png" />][cssplaylist]
[<img align="left" alt="JavaScript" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png" />][jsplaylist]
[<img align="left" alt="Git" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png" />][webdevplaylist]
[<img align="left" alt="GitHub" width="26px" src="https://raw.githubusercontent.com/github/explore/78df643247d429f6cc873026c0622819ad797942/topics/github/github.png" />][webdevplaylist]
[<img align="left" alt="Terminal" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/terminal/terminal.png" />][webdevplaylist]

<br />
<br />

---

### Authors

Andreu Jové



---

### License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the LICENSE.md file for details.