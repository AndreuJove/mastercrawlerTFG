import json 

with open('tools.json', "r") as fp:
    jsonData = json.load(fp)
    
urlToolList, idToolList, nameToolList = ([] for i in range(3))      
           
tools = jsonData[1]['tools']
lessTools = tools[:20]

print("Less tools has: {}".format(len(lessTools)))
def getAllFromJson(toolsList):
    toolsListOut = []
    for tool in toolsList:
        dict_tool = {}
        idTool = tool["@id"]
        numberOfDashes = idTool.count('/')
        if numberOfDashes <= 5:
            urlTool = tool["web"]["homepage"]
            if urlTool not in urlToolList:
                dict_tool['name'] = tool["name"]
                dict_tool['url'] = tool["web"]["homepage"]
                dict_tool['id'] = tool["@id"]
                toolsListOut.append(dict_tool)       
    return toolsListOut            

# def getUrlListFromTools(toolsListOut):
#     toolUrlList = []
#     for tool in toolsListOut:
#         toolUrlList.append(tool['url'])
#     return toolUrlList



toolsListOut = getAllFromJson(lessTools)
#toolUrlList = getUrlListFromTools(toolsListOut)

# print(toolUrlList)
# print(len(toolUrlList))

# print(toolsListOut)
# print(len(toolsListOut))


# import logging
# logging.getLogger('scrapy').setLevel(logging.WARNING)
# with open('tools.json', "r") as fp:
#     jsonData = json.load(fp)
# urlToolList, idToolList, nameToolList = ([] for i in range(3))             
# tools = jsonData[1]['tools']
# lessTools = tools[:10]
# def getAllFromJson(toolsList):
#     for tool in toolsList:
#         urlTool = tool["web"]["homepage"]
#         numberOfDashes = urlTool.count('/')
#         if numberOfDashes <= 5:
#             if urlTool not in urlToolList:
#                 nameToolList.append(tool["name"])
#                 urlToolList.append(urlTool) 
#                 idToolList.append(tool["@id"])  
#     return urlToolList, idToolList, nameToolList            
# urlToolList, idToolList, nameToolList = getAllFromJson(lessTools)
