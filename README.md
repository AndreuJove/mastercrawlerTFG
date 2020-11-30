
## Crawler description:
- This crawler aims to determinate the status (HTTP Codes, Exceptions) and collect the HTMLS without JavaScript from the websites of a dataset of bioinformatic tools.<br />

### Input:
- File that has to contain an array of websites for crawling.<br />

### Output:
- JSON file called by default "manifest_tools_scrapy.json" inside the directory output_data that follows the next JSON schema. 

```
manifest_tools.json = {
  'tools_ok' : [
                        {
                        "final_url": type="string",
                        "first_url": type="string"
                        "path_file": type="string"
                        },

                ...
  ],
  'stats' : 
                        {
                         "log_count/INFO": type="integer",
                        "start_time": type="string",
                        "memusage/startup": type="integer",
                        ...

                        },
                        
        
```

- JSON file called by default "entry_n.json" inside the directory of htmls_no_js that follows the next JSON schema. 

```

entry_n.json = {
  'id' : type="string",
 
  'html_no_js' : type="string"
                        
}
```
<br />

## Package installation:

1) Open terminal.
2) Go to the current directory where you want the cloned directory to be added using 'cd'.
3) Run the command: <br />
        $ git clone https://github.com/AndreuJove/mastercrawlerTFG.
4) Install requirements.txt: <br />
        $ pip3 install -r requirements.txt
5) From root directory and run the following command:<br />
        $ python3 main.py
6) The name of the output files and the directory to save them can be changed using the following      command line (write it with the default values):<br />
        $ python3 main.py <br />
        i_path_file ../websites_filter/output_data/websites_to_crawl.json <br />
        -o_directory output_data <br />
        -filename_output manifest_tools_scrapy <br />
        -o_directory_htmls_no_js htmls_no_js <br />
        -log_file_name crawler <br />
<br />


## Build with:
- [Scrapy](https://docs.scrapy.org/en/latest/) - Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.
- [Pydispatcher](https://grass.osgeo.org/grass79/manuals/libpython/pydispatch.html) - Multiple-producer-multiple-consumer signal-dispatching
- [Twisted](https://readthedocs.org/projects/twisted/) - Twisted is an event-driven networking engine written in Python and licensed under the open source.
- [Argparser](https://docs.python.org/3/library/argparse.html) - The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments.
- [Logging](https://docs.python.org/3/howto/logging.html) - Logging is a means of tracking events that happen when some software runs. The software’s developer adds logging calls to their code to indicate that certain events have occurred.

<br />


## Authors

- Andreu Jové

<br />


## License

- This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE.MD](https://github.com/AndreuJove/mastercrawlerTFG/blob/master/LICENSE.md) file for details.