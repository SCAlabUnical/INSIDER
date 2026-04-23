import matplotlib.pyplot as plt
import simpn.visualisation as vis
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp
from random import uniform
from simpn.reporters import Reporter
from WorkflowManager import WorkflowManager

import json
# Opening JSON file
f = open('json/iiot.json')
# returns JSON object as a dictionary
data = json.load(f)

# Instantiate a simulation problem.
workflow = SimProblem()

nomi = {'Device':'None', 'Communication':'NETWORK', 'Computation':'COMPUTE', 'Storage':'STORAGE'}

listaNomi = []

places = {}

listaNomi = []

# Iterating through the json list
for elem in data['nodes']:
    listaNomi.append(str(elem["id"])+"_"+elem["name"])

    if elem['type'] == 'Device':
        auxVar = WorkflowManager.insider_add_var(workflow, {"name": str(elem["id"])+"_"+elem["name"],
                                                            "type": "None",
                                                            "labelName":"yes"})
    else:
        auxVar = WorkflowManager.insider_add_var(workflow, {"name": str(elem["id"])+"_"+elem["name"],
                                                            "type": nomi[elem['type']],
                                                            "labelName":"no"})
    # Aggiungo un token per ogni posto
    #auxVar.put(str(elem["id"])+"_"+elem["name"])
    places[elem["id"]] = auxVar

#print(listaNomi)

for elem in data['connections']:
    #print(elem["source"]["nodeID"], "-->",elem["dest"]["nodeID"])

    def Transaction(c):
        return [SimToken(c, delay=exp(3)*60)]

    #type = places[elem["dest"]["nodeID"]].insider_tag['type']
    type = str(places[elem["dest"]["nodeID"]].insider_tag['type'])
    name = str(places[elem["dest"]["nodeID"]].get_id())

    while name in listaNomi:
        name = "_"+name
    listaNomi.append(name)
    #print(listaNomi)

    WorkflowManager.insider_add_event(workflow, [places[elem["source"]["nodeID"]]],
                                      [places[elem["dest"]["nodeID"]]], Transaction,
                                      {"name":name,"type":type})


##### VISUALISATION
from insidervisualization import Visualisation
layoutWF = "./Layout/Parser.txt"
v = Visualisation(workflow, layoutWF)
v.show("Parser")
v.save_layout(layoutWF)

