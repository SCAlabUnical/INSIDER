import json

with open('json/iiot.json') as json_file:
    dataIn = json.load(json_file)
    #print(dataIn)

json_file = open("json/iiot_formatted.json", "w")
json_file.write(json.dumps(dataIn, indent=4))
json_file.close()