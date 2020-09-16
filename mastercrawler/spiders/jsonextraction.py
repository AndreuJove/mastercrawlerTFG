import json
import time
import os
import pandas as pd
"""
Collect all problematic URLs for crawling and group different tools that have same URLs.

The ouput are: list of problematic URLs and list of tools with unique URLs for crawling.

This code only run ones. For the first check of the dataset.

Command line to download the dataset of tools. First move with cd.. to input_data directory and run this command:

wget "https://dev-openebench.bsc.es/monitor/rest/edam/aggregate?projection=description&projection=web&name=&label=null" -O final_tools_vicky_api.json

"""

rel_path_output = '../output_data/tools_list_unique_url.json'
if not os.path.exists(rel_path_output):
    start = time.time()

    # Open file of tools. This file is a list of dictionaries. Finally load to the variable jsonInput_data.
    rel_path_input_data = "../input_data/final_tools_v_api.json"
    with open(rel_path_input_data, "r") as fp:
        jsonInput_data = json.load(fp)

    # Create a dictionary with 3 pairs of key : value. Keys are: first_url_tool, name and id.
    def create_dict_item(url, name, id):
        dict_tool = {}
        dict_tool['first_url_tool'] = url
        dict_tool['name'] = name
        dict_tool['id'] = id
        return dict_tool

    # Counter of different domains in dataset.
    domains_counter = {}
    def counter_domains(url):
        domain = url.split("://")[-1].split("/")[0].replace("www.", "").lower()
        if domain in domains_counter:
            domains_counter[domain] += 1
        else:
            domains_counter[domain] = 1

    def getAllFromJson(toolsList):
        """
        Extracts website/homepage, id, name from dataset.

        Identify the problematic URLs for crawling.

        Check the repeated URLs in different tools and group their ids and names.

        The output is a list of dictionaries which each dict has url, id/s, name/s.
        """
        tools_list_unique_url = []
        problematic_url = []
        for index, tool in enumerate(toolsList):
            passing = True
            first_url_tool = tool["entities"][0]['tools'][0]["web"]["homepage"]
            idTool = tool["entities"][0]['tools'][0]["@id"]
            nameTool = tool["entities"][0]['tools'][0]["name"]
            counter_domains(first_url_tool)
            if first_url_tool.endswith(".zip") or first_url_tool.endswith(".pdf") or first_url_tool.endswith(".mp4") or first_url_tool.endswith(".gz") or first_url_tool.endswith(".bz2") or first_url_tool.startswith("ftp://") or len(first_url_tool) < 7:
                problematic_url.append(create_dict_item(
                    first_url_tool, nameTool, idTool))
                continue
            if not first_url_tool.startswith("http"):
                first_url_tool = "https://www." + first_url_tool
            if tools_list_unique_url:
                for i, k in enumerate(tools_list_unique_url):
                    if k['first_url_tool'] == first_url_tool:
                        passing = False
                        if type(k['name']) is str:
                            tools_list_unique_url[i]['name'] = [
                                tools_list_unique_url[i]['name']]
                            tools_list_unique_url[i]['id'] = [
                                tools_list_unique_url[i]['id']]
                        tools_list_unique_url[i]['name'].append(nameTool)
                        tools_list_unique_url[i]['id'].append(idTool)
                        continue
            if passing:
                tools_list_unique_url.append(
                    create_dict_item(first_url_tool, nameTool, idTool))
        return tools_list_unique_url, problematic_url
    tools_list_unique_url, problematic_url = getAllFromJson(jsonInput_data)

    # Create Dataframe of the counter of domains:
    df = pd.DataFrame(domains_counter.items(), columns=[
                      "Domain", "Count"]).sort_values(by='Count', ascending=False)[:36]

    # Primary classification of domains:
    university = ['ncbi.nlm.nih.gov', 'ebi.ac.uk',
                  'broadinstitute.org', 'csbio.sjtu.edu.cn', 'dna.leeds.ac.uk']
    institucional = ['cbs.dtu.dk', 'galaxy.pasteur.fr', 'bioinformatics.psb.ugent.be', 'zhanglab.ccmb.med.umich.edu', 'jci-bioinfo.cn',
                     'sanger.ac.uk', 'protein.bio.unipd.it',  'imgt.org', 'genius.embnet.dkfz-heidelberg.de',
                     'bioinformatics.psb.ugent.be', 'ccb.jhu.edu', 'tools.proteomecenter.org', 'genome.sph.umich.edu']
    lifeScience = ['bioconductor.org', 'emboss.open-bio.org']
    collections = ['bioinformatics.org', 'ms-utils.org', 'web.expasy.org']
    generic = ['github.com', 'cran.r-project.org', 'doi.org', 'imtech.res.in', 'pypi.python.org',
               'sourceforge.net', 'sites.google.com', 'metacpan.org', 'gitlab.com', 'code.google.com', 'bitbucket.org']

    # Create list of dictionaries to save in json format:
    list_domains_and_grouptations = [
        {'domains': df['Domain'].tolist()},
        {'values_domains':  df['Count'].tolist()},
        {'university': university},
        {'institucional': institucional},
        {'lifeScience': lifeScience},
        {'collections': collections},
        {'generic': generic}
    ]

    # Safe list of dictionaries about domains, domains_count, groupation in jsonfile.
    with open('../output_data/domains_and_groupations.json', 'w') as f:
        json.dump(list_domains_and_grouptations, f)

    # Safe tools lists for scrapy crawler in json format:
    with open('../output_data/tools_list_unique_url.json', 'w') as fout:
        json.dump(tools_list_unique_url, fout)

    # Safe problematic tools for scrapy crawler in json format:
    with open('../output_data/problematic_tools.json', 'w') as out:
        json.dump(problematic_url, out)

    print(f"Tools URL unique: {len(tools_list_unique_url)}")
    print(f"Problematic tools: {len(problematic_url)}")

    end = time.time()
    print(f"Time of execution: {end - start}")
