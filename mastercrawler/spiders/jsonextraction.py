import json 
import time
start = time.time()

#wget "https://dev-openebench.bsc.es/monitor/rest/edam/aggregate?projection=description&projection=web&name=&label=null" -O final_tools_vicky_api.json

rel_path = "../input_data/final_tools_vicky_api.json"

with open(rel_path, "r") as fp:
    jsonInput_data = json.load(fp)   

lessTools = jsonInput_data

def create_dict_item(url, name, id):
    dict_tool = {}
    dict_tool['first_url_tool'] = url
    dict_tool['name'] = name
    dict_tool['id'] = id
    return dict_tool

def getAllFromJson(toolsList):
    tools_list_unique_url = []
    problematic_url = []
    for index,tool in enumerate(toolsList):
        passing = True    
        first_url_tool = tool["entities"][0]['tools'][0]["web"]["homepage"]
        idTool = tool["entities"][0]['tools'][0]["@id"]
        nameTool = tool["entities"][0]['tools'][0]["name"]
        if first_url_tool.endswith(".zip") or first_url_tool.endswith(".pdf") or first_url_tool.endswith(".mp4") or first_url_tool.endswith(".gz") or first_url_tool.endswith(".bz2") or first_url_tool.startswith("ftp://") or len(first_url_tool)<7:
            problematic_url.append(create_dict_item(first_url_tool,nameTool, idTool))
            continue
        if not first_url_tool.startswith("http"):
                first_url_tool = "https://www." + first_url_tool
        if tools_list_unique_url:
            for i, k in enumerate(tools_list_unique_url):
                if k['first_url_tool'] == first_url_tool:
                    passing = False
                    if type(k['name']) is str:
                        tools_list_unique_url[i]['name'] = [tools_list_unique_url[i]['name']] 
                        tools_list_unique_url[i]['id'] = [tools_list_unique_url[i]['id']]
                    tools_list_unique_url[i]['name'].append(nameTool)
                    tools_list_unique_url[i]['id'].append(idTool)
                    continue
        if passing:
            tools_list_unique_url.append(create_dict_item(first_url_tool,nameTool, idTool))  
    return tools_list_unique_url, problematic_url            

tools_list_unique_url, problematic_url = getAllFromJson(lessTools)

with open('../input_data/tools_list_unique_url.json', 'w') as fout:
    json.dump(tools_list_unique_url, fout)

with open('../output_data/problematic_url.json', 'w') as out:
    json.dump(problematic_url, out)

print(f"Tools URL unique: {len(tools_list_unique_url)}")
print(f"Problematic tools: {len(problematic_url)}")

end = time.time()
print(end - start)
