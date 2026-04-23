import os

import json
import matplotlib.pyplot as plt
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp
from random import uniform
from simpn.reporters import Reporter
from WorkflowManager import WorkflowManager

# Opening JSON file
f = open('json/iiot.json')
# returns JSON object as a dictionary
data = json.load(f)

# Instantiate a simulation problem.
workflow = SimProblem()

nameTaskTypeMapping = {'Device': 'None', 'Communication': 'NETWORK', 'Computation': 'COMPUTE', 'Storage': 'STORAGE'}

nameList = []

places = {}
event = {}

scale = 0.66

def tranPosition( x1, y1, x2, y2 ):

    if x1 < x2:
        posX = x1 + (x2-x1)/2
    else:
        posX = x2 + (x1-x2)/2

    if y1 < y2:
        posY = y1 + (y2-y1)/2
    else:
        posY = y2 + (y1-y2)/2

    posX = int(posX)
    posY = int(posY)

    #print(posX, posY,x1,x2,y1,y2)

    return posX, posY


# Iterating through the json list
for elem in data['nodes']:

    nameList.append(str(elem["id"]) + "_" + elem["name"])

    if elem['type'] == 'Device':
        auxVar = WorkflowManager.insider_add_var(workflow, {"name": str(elem["id"])+"_"+elem["name"],
                                                            "type": "None",
                                                            "labelName":"yes"})
    else:
        auxVar = WorkflowManager.insider_add_var(workflow, {"name": str(elem["id"])+"_"+elem["name"],
                                                            "type": nameTaskTypeMapping[elem['type']],
                                                            "labelName":"no"})
    auxVar.X = int(elem["x"]*scale)
    auxVar.Y = int(elem["y"]*scale)

    # Aggiungo un token per ogni posto
    #auxVar.put(str(elem["id"])+"_"+elem["name"])
    auxVar.tansaction = False

    places[elem["id"]] = auxVar

for elem in data['connections']:
    #print(elem["source"]["nodeID"], "-->",elem["dest"]["nodeID"])

    def Transaction(c):
        return [SimToken(c, delay=exp(3)*60)]

    type = places[elem["source"]["nodeID"]].insider_tag['type']
    name = str(places[elem["source"]["nodeID"]].get_id())

    ## Aggiungo "_" all'inizio del nome, fino a renderlo univoco
    while name in nameList:
        name = "_"+name
    nameList.append(name)
    #print(listaNomi)

    ev = WorkflowManager.insider_add_event(workflow, [places[elem["source"]["nodeID"]]],
                                          [places[elem["dest"]["nodeID"]]], Transaction,
                                          {"name":name,"type":type})

    ev.X , ev.Y = tranPosition(places[elem["source"]["nodeID"]].X,
                               places[elem["source"]["nodeID"]].Y,
                               places[elem["dest"]["nodeID"]].X,
                               places[elem["dest"]["nodeID"]].Y    )

    places[elem["source"]["nodeID"]].tansaction = True

    event[name] = ev

for key in places:
    if places[key].tansaction == False:
        ev = WorkflowManager.insider_add_event(workflow, [places[key]],
                                               [], Transaction,
                                               {"name":places[key].get_id()+"_t","type":places[key].insider_tag['type']})

layoutWF = "./Layout/ParserXY.txt"

if not os.path.isfile(layoutWF):
    lwf = open(layoutWF, "w")
    lwf.write( "1400,700\n")

    for key in places:
        lwf.write( str(places[key]._id) + "," + str(places[key].X) + "," + str(places[key].Y) + "\n" )
    for key in event:
        lwf.write( str(event[key]._id) + "," + str(event[key].X) + "," + str(event[key].Y) + "\n" )

    lwf.close()

##### VISUALISATION
from insidervisualization import Visualisation
v = Visualisation(workflow, layoutWF)
v.show("ParserXY")
v.save_layout(layoutWF)

