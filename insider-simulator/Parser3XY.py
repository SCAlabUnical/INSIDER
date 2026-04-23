import os

import json
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp

from WorkflowManager import WorkflowManager

# Opening JSON file
f = open('json/iiot.json')
# returns JSON object as a dictionary
data = json.load(f)

# Instantiate a simulation problem.
workflow = SimProblem()

# nameTaskTypeMapping = {'Device': 'None', 'Communication': 'NETWORK', 'Computation': 'COMPUTE', 'Storage': 'STORAGE'}
nameTaskTypeMapping = {'Device': 'COMPUTE', 'Communication': 'COMPUTE', 'Computation': 'COMPUTE', 'Storage': 'STORAGE'}

nameList = []

places = {}
event = {}

scale = 1.5

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

def Transaction(c):
    return [SimToken(c, delay=exp(3)*60)]


# Iterating through the json list
for elem in data['nodes']:
    type = nameTaskTypeMapping[elem['type']]
    name_p = str(elem["id"])+"_"+elem["name"]+"_p"
    nameList.append(name_p)
    auxVar = WorkflowManager.insider_add_var(workflow, {"name": name_p ,"type": type,"labelName":"no"})
    auxVar.X = int(elem["x"]*scale)
    auxVar.Y = int(elem["y"]*scale)
    places[elem["id"]] = auxVar


for elem in data['connections']:
    print(elem["source"]["nodeID"],"-",elem["dest"]["nodeID"])
    #type = str(places[elem["source"]["nodeID"]].insider_tag['type'])
    type = "NETWORK"
    name_p = str(places[elem["source"]["nodeID"]].get_id())+"_p"
    shiftX = 150
    shiftY = 0
    while name_p in nameList:
        name_p = "_"+name_p
        shiftY += 100
    nameList.append(name_p)
    auxVar = WorkflowManager.insider_add_var(workflow, {"name": name_p ,"type": type,"labelName":"no"})
    auxVar.X = int(places[elem["source"]["nodeID"]].X+shiftX)
    auxVar.Y = int(places[elem["source"]["nodeID"]].Y+shiftY)

    places[elem["source"]["nodeID"]].successors.append(name_p)
    auxVar.successors.append( elem["dest"]["nodeID"] )

    places[ name_p ] = auxVar


for key in places.keys():

    labelName = "no"
    if places[key].insider_tag["type"] != "NETWORK":
        labelName = "yes"
    type = places[key].insider_tag["type"]
    name = places[key].get_id() + "_t"

    outflow = []
    for iter in places[key].successors:
        outflow.append(places[iter])

    ev = WorkflowManager.insider_add_event(workflow,
                                           [places[key]],
                                           outflow,
                                           Transaction,
                                           {"name":name,"type":type,"labelName":labelName} )

    # ev.X , ev.Y = tranPosition(places[key].X,
    #                            places[key].Y,
    #                            places[places[key].succ].X,
    #                            places[places[key].succ].Y    )

    event[name] = ev


layoutWF = ("./Layout/Parser3XY.txt")

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
v.show("Parser3XY")
v.save_layout(layoutWF)

