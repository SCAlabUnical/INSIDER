import os

import json
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp

from WorkflowManager import WorkflowManager

############### Opening JSON file
f = open('json/BeltWasteRecyclingV1_json.json')
# returns JSON object as a dictionary
data = json.load(f)


############### Instantiate a simulation problem.
workflow = SimProblem()


############### Dizionari per posti e transizioni (event)
places = {}
event = {}


############### Transizione di default
def Transaction(c,r):
    return [SimToken(c, delay=exp(3)*60)]


############### Dizionario contenente key (sorgente) e value (lista destinazioni)
connections = dict()
for elem in data['connections']:
    if elem[ "source"] in connections:
        connections[ elem[ "source" ] ].append( elem[ "dest" ] )
    else:
        connections[ elem[ "source" ] ] = [ elem[ "dest" ] ]


############### Crezione dei posti una per nodo del file json
for elem in data['nodes']:
    type = elem['type']
    name_p = elem["name"] + "_p"
    name_r = elem["resource"] +"_r"

    auxVar_p = WorkflowManager.insider_add_var(workflow, {"name": name_p ,"type": type,"labelName":"no"})
    auxVar_p.X = elem["x"]
    auxVar_p.Y = elem["y"]
    places[name_p] = auxVar_p

    if name_r not in places:
        auxVar_r = WorkflowManager.insider_add_var(workflow, {"name": name_r ,"type": type,"labelName":"yes"})
        auxVar_r.X = elem["x"] + 100
        auxVar_r.Y = elem["y"] - 100
        places[name_r] = auxVar_r


############### Creazione delle transizioni una per nodo del file json
for elem in data['nodes']:
    type = elem['type']
    name_p = elem["name"] + "_p"
    name_r = elem["resource"] +"_r"

    auxVar_p = places[name_p]
    auxVar_r = places[name_r]

    outflow = [] # lista destinazioni della transizione corrente
    if elem["name"] in connections: # non è il nodo collector
        for conn in connections[elem["name"]]:
            outflow.append(places[  conn + "_p"])

    ev = WorkflowManager.insider_add_event(workflow,
                                           [ auxVar_p, auxVar_r ],
                                           outflow,
                                           Transaction,
                                           {"name":elem["name"],"type":type,"labelName":"yes","flow":elem["flowout"][1]} )

    ev.X = elem["x"] + 100
    ev.Y = elem["y"]

    event[elem["name"]] = ev


############# Creazione del file Layout per la visualizzazione
layoutWF = ("./Layout/Parser4XY.txt")

if not os.path.exists(layoutWF):
    lwf = open(layoutWF, "w")
    lwf.write( "1400,700\n")

    for key in places:
        lwf.write( str(places[key]._id) + "," + str(places[key].X) + "," + str(places[key].Y) + "\n" )
    for key in event:
        #print("key:",key,"value:",event[key])
        lwf.write( str(event[key]._id) + "," + str(event[key].X) + "," + str(event[key].Y) + "\n" )

    lwf.close()

############# VISUALISATION
from insidervisualization import Visualisation
v = Visualisation(workflow, layoutWF)
v.show("Parser4XY")
v.save_layout(layoutWF)

