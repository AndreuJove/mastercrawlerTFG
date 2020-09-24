

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



nlp-standard-preprocessing
This component runs a standard preprocessing nlp process.

Description
It uses the Stanford CoreNLP for:
Sentence Splitting, Tokenization, Part of Speech (POS), other features: word types, lemma, kinds, formats, lenght and masks.
Also add the Stanford Dependency Parser (depparse) for each sentence as a feature in the Sentence Annotation.
The input folder can contain plain files or XML Gate files.
The output will be in GATE format and the annotations will be grouped into an specific annotation set provided.
The component can be run with a specific thread number. In that case the files will be splited in t number of threads for data paralelization.

Actual Version 1.4, 2020-09-16

Changelog


Docker
javicorvi/nlp-standard-preprocessing

Build and Run the Docker
#To build the docker, just go into the nlp-standard-preprocessing folder and execute
docker build -t nlp-standard-preprocessing .
#To run the docker, just set the input_folder and the output
mkdir ${PWD}/nlp_preprocessing_output; docker run --rm -u $UID -v ${PWD}/input_output:/in:ro -v ${PWD}/nlp_preprocessing_output:/out:rw nlp-standard-preprocessing nlp-standard-preprocessing -i /in -o /out	-a MY_SET
Parameters:

-i input folder with the documents to annotated. The documents could be plain txt or xml gate documents.


-o output folder with the documents annotated in gate format.


-a annotation set where the annotation will be included.


-annotators. Stanford Core NLP Annotators to be run, by default: tokenize, ssplit, pos, lemma, ner.


-t or threads. Number of threads to run the preprocessing task. It will divide the the input documents by threads. 

## Built With


Docker - Docker Containers

Maven - Dependency Management

StanfordCoreNLP - Stanford CoreNLP – Natural language software

GATE - GATE: a full-lifecycle open source solution for text processing


Versioning
We use SemVer for versioning. For the versions available, see the tags on this repository.

Authors

Javier Corvi


License
This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the LICENSE.md file for details