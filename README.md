

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
