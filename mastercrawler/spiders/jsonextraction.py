import json 

with open('finaltools.json', "r") as fp:
    jsonData = json.load(fp)
    
#urlToolList, idToolList, nameToolList = ([] for i in range(3))      

lessTools = jsonData[50:70]

def getAllFromJson(toolsList):
    toolsListOut = []
    problematic_url = []

    for index,tool in enumerate(toolsList):
        dict_tool = {}
        
        idTool = tool["entities"][0]['tools'][0]["@id"]
        urlTool = tool["entities"][0]['tools'][0]["web"]["homepage"]
        nameTool = tool["entities"][0]['tools'][0]["name"]
        if urlTool.endswith(".zip") or urlTool.endswith(".pdf") or urlTool.endswith(".mp4") or urlTool.endswith(".gz") or urlTool.startswith("ftp://") or len(urlTool)<7:
            dict_tool['url'] = urlTool
            dict_tool['name'] = nameTool
            dict_tool['id'] = idTool
            problematic_url.append(dict_tool)
            continue
        if not urlTool.startswith("http"):
                urlTool = "https://www." + urlTool
        if toolsListOut and toolsListOut[-1]['url'] == urlTool:
            if type(toolsListOut[-1]['name']) is str:
                toolsListOut[-1]['name'] = [toolsListOut[-1]['name']]
                toolsListOut[-1]['id'] = [toolsListOut[-1]['id']]
            toolsListOut[-1]['name'].append(nameTool)
            toolsListOut[-1]['id'].append(idTool)
            continue
        dict_tool['url'] = urlTool
        dict_tool['name'] = nameTool
        dict_tool['id'] = idTool
        toolsListOut.append(dict_tool)  
    return toolsListOut, problematic_url            

toolsListOut, problematic_url = getAllFromJson(lessTools)

print(len(toolsListOut))

#print(problematic_url)
for tool in problematic_url:
    print("_----------------------------------------")
    print(tool)