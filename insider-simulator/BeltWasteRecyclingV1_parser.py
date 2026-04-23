import collections
import random
from logging import raiseExceptions

import matplotlib.pyplot as plt
import numpy as np
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp
from simpn.reporters import Reporter
from WorkflowManager import WorkflowManager
from Resource import Node
from Task import Task
import csv
import json



######## PARAMETRI SIMULATORE ##################################################################

name_token = "Req_"
inputAverageArrivalTime = 2.0 # secondi
SIMULATION_DURATION = 1*10*60 # secondi = ore*minuti*secondi
rhoCount = dict()
resourceUtilizationTime=dict()
requestUtilizationTimeTaskSeq=dict()



######## Funzioni di utilità #####################################################################

def getTasktype(tt):
    if "Tc".lower() == tt.lower():
        return 0
    elif "Tn".lower() == tt.lower():
        return 1
    elif "Ts".lower() == tt.lower():
        return 2
    else:
        raise ValueError("Task type not recognized")


def getServiceTime(nameTask, nameToken, tasks):

    for task in tasks:
        #print("---",nameTask)
        #print("--------",task.name)
        if task.name == nameTask:
            increment = 1.00 + random.random()/10
            if task.type == 0:
                duration = increment * task.requestMilionsOfInstructions/task.executor.MIPS
                #print("----0:",duration,nameTask)
                break
            elif task.type == 1:
                duration = increment * task.requestTransferMB/task.executor.uploadSpeed
                #print("---1:",duration,nameTask)
                break
            elif task.type == 2:
                duration = increment * task.requestStoreMB/task.executor.querySpeedWrite
                #print("---2:",duration,nameTask)
                break
            else:
                raise ValueError("Task type not recognized")
    else:
        raise ValueError("Task not found")

    if nameTask in rhoCount:
        rhoCount[nameTask] = rhoCount[nameTask] + duration
    else:
        rhoCount[nameTask] = duration

    return duration

def updateReourceUtilizationTime(nameToken,duration):
    if nameToken[0] in resourceUtilizationTime:
        # se la richiesta già esiste aggiungo la duration corrente al totale
        resourceUtilizationTime[nameToken[0]] = resourceUtilizationTime[nameToken[0]] + duration
    else:
        # alrimenti creo la richiesta e gli setto la duration corrente
        resourceUtilizationTime[nameToken[0]] = duration

def updaterRequestUtilizationTimeTaskSeq(nameToken,duration):
    if nameToken in requestUtilizationTimeTaskSeq:
        # se la richiesta già esiste aggiungo la duration corrente al totale
        requestUtilizationTimeTaskSeq[nameToken] = requestUtilizationTimeTaskSeq[nameToken] + duration
    else:
        # alrimenti creo la richiesta e gli setto la duration corrente
        requestUtilizationTimeTaskSeq[nameToken] = duration



######### Read data from file ##################################################################

# Importazione dei dati delle risorse da file
Resources = []
with open('data/Resources.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if spamreader.line_num == 1:
            continue

        auxNode = Node(spamreader.line_num-1,0)
        ####### Nc #######
        auxNode.cpuFrequency = float(row[3])
        auxNode.cpuCores = float(row[2])
        auxNode.freeFrequency = auxNode.cpuCores * auxNode.cpuFrequency
        auxNode.MIPS = auxNode.cpuCores * auxNode.cpuFrequency * 1000
        auxNode.ram = float(row[5])
        auxNode.freeRam = float(row[5])
        ####### Tn #######
        auxNode.bandwidth = -1
        auxNode.uploadSpeed =float( row[12])
        auxNode.downloadSpeed = float(row[12])
        ####### Ts #######
        auxNode.querySpeedRead = float(row[14])
        auxNode.querySpeedWrite = float(row[14])

        Resources.append(auxNode)

# print resources
for element in Resources:
    print("Resource:",element.__dict__) # o.__dict__

# Importazione dei dati dei task da file
Tasks = []
with open('data/Tasks.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if spamreader.line_num == 1:
            continue

        auxTask = Task(spamreader.line_num-1,getTasktype(row[0]))

        auxTask.name = row[1]

        if auxTask.type == 0:
            auxTask.requestMilionsOfInstructions = float(row[2])
        elif auxTask.type == 1:
            auxTask.requestTransferMB = float(row[2])
        elif auxTask.type == 2:
            auxTask.requestStoreMB = float(row[2])
        else:
            raise ValueError("Task type not recognized")


        Tasks.append(auxTask)

#print tasks
for element in Tasks:
    print("Task:",element.__dict__) # o.__dict__


# ramdom scheduling
allocation = []
with open('data/Allocation.csv', newline='') as csvfile:
    allocationFile = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in allocationFile:
        allocation.append(row)

print("Allocation:", allocation)

for elemTask in Tasks:
    for elemAllocationRow in allocation:
        for elem in elemAllocationRow:
            if elemTask.name == elem:
                elemTask.executor = Resources[int(elemAllocationRow[0])]


# print allocation
for element in Tasks:
    print("Task:",element.name, " on Resources:", element.executor.__dict__)



########## Create workflow ######################################################################

# Instantiate a simulation problem.
workflow = SimProblem()


######### Timer per statistiche da rimuovere #####################################################
Timer_p = WorkflowManager.insider_add_var(workflow, {"name": "Timer_p", "type": ""})
Timer_p.put("Timer")
def Timer_t(c):
    return [SimToken(c, delay=1)]
WorkflowManager.insider_add_event(workflow,[Timer_p],[Timer_p], Timer_t,
                                  {"name":"Timer","type":""})


##########################  PARSER Start #########################################################

def getFlow(connections, nameTask):
    inFlow = []
    outFlow = []
    for connection in connections:
        #print("con:",connection["source"],connection["dest"])
        if connection["source"] == nameTask:
            outFlow.append(connection["dest"])
        if connection["dest"] == nameTask:
            inFlow.append(connection["source"])
    return inFlow, outFlow

f = open('json/BeltWasteRecyclingV1_json.json')
jsonData = json.load(f)

places = {}
for node in jsonData['nodes']:
    type = node['type']
    inFlow, outFlow = getFlow(jsonData["connections"],node['nameTask'])
    for plcs in inFlow:
        if plcs not in places:
            if plcs == node["resource"][0]:
                auxVar_p = WorkflowManager.insider_add_var(workflow, {"name": plcs ,"type": type,"resource":node["resource"]})
            else:
                auxVar_p = WorkflowManager.insider_add_var(workflow, {"name": plcs ,"type": type})
            places[plcs] = auxVar_p

# Creo il primo token per la generazione di tutti gli altri
# da sistemare meglio con primo token da json



def createTransationFromJsonNode(node):
    inputTransation = ""
    outputTransation = ""

    inFlow, outFlow = getFlow(jsonData["connections"],node['nameTask'])

    for i in range(len(inFlow)):
        if inputTransation == "":
            inputTransation += "in"+str(i+1)
        else:
            inputTransation += ",in"+str(i+1)

    for i in range(len(outFlow)-1):
        if outputTransation == "":
            outputTransation += "SimToken("+ "in1" +", delay=duration)"
        else:
            outputTransation += ", SimToken("+ "in1"  +", delay=duration)"
    if len(outFlow) > 1:
        outputTransation += ", SimToken( in"+ str(len(inFlow)) +", delay=duration)"

    if node["type"] == "BEGIN":
        places[node["start"]].put(name_token + str(1))
        print(f"""def {node["name"]}({inputTransation}):
                     next_token=((int)(in1.replace(name_token, "")))+1
                     return [SimToken(name_token+str(next_token), delay=inputAverageArrivalTime),SimToken(in1, delay=0)]""")
        exec(f"""def {node["name"]}({inputTransation}):
                     print("in1:",in1)
                     next_token=((int)(in1.replace(name_token, "")))+1
                     return [SimToken(name_token+str(next_token), delay=inputAverageArrivalTime),SimToken(in1, delay=0)]""", globals())

    else:
        print(f"""def {node["name"]}({inputTransation}):
                     print("in1:",type(in1),"in2:",type(in2))
                     duration = getServiceTime("{node["nameTask"]}", in1, Tasks)
                     updateReourceUtilizationTime(in{len(inFlow)}, duration)
                     updaterRequestUtilizationTimeTaskSeq(in1,duration)
                     return [{outputTransation}]""")
        exec(f"""def {node["name"]}({inputTransation}):
                     duration = getServiceTime("{node["nameTask"]}", in1, Tasks)
                     updateReourceUtilizationTime(in{len(inFlow)}, duration)
                     updaterRequestUtilizationTimeTaskSeq(in1,duration)
                     return [{outputTransation}]""", globals())


for node in jsonData['nodes']:

    createTransationFromJsonNode(node)
    inFlow, outFlow = getFlow(jsonData["connections"],node['nameTask'])

    # guard=lambda c1, c2,c3, c4: c1 == c2 == c3 == c4
    guard = "None"
    if node["flowin"][0] == "join" and node["flowin"][1] == "and":
        guard = "guard=lambda in1"
        for i in range(1,len(inFlow)):
            guard += ",in"+str(i+1)
        guard = guard + " : in1"
        for i in range(1,len(inFlow)):
            guard += "==in"+str(i+1)
    print(guard)
    guardF = exec(guard)

    inf = []
    for pname in inFlow:
        inf.append(places[pname])
    outf = []
    for pname in outFlow:
        outf.append(places[pname])
    WorkflowManager.insider_add_event(workflow, inf,outf, globals()[node["name"]],
                                      {"name":node["name"],"type":node["type"]}, guard=guardF)


##########################  PARSER End ############################################################


#########################################

######### Run simulation ################

## Reporter statistics
#
class InsiderReporter(Reporter):

    def __init__(self):

        self.arrival_times = dict()
        self.start_times = dict()
        self.complete_times = dict()
        self.total_proc_time = 0
        self.wait_time_x_workflow= dict()
        self.wait_time_x_task= dict()
        self.time_num_token_in_workflow = [0] * SIMULATION_DURATION
        self.wait_length_x_task = dict()

    def callback(self, timed_binding):
        (binding, time, event) = timed_binding
        #print("-------",binding,"-------", time,"-------", event)
        #print("XXX:",binding[0][1].value)
        #print("###")
        #print(timed_binding)
        #print(binding)
        #print(BeltWasteRecyclingConRisorsa)
        #print("---")
        #print(timed_binding)
        #print(binding[0][0])
        #print(binding[0][1])
        #print(binding[0][1].time)
        #print(time)
        #print(event)

        if event.get_id() == "Source":
            c_id = binding[0][1].value
            #print(c_id)
            self.arrival_times[c_id] = time
            for i in range(int(time),SIMULATION_DURATION):
                self.time_num_token_in_workflow[i]+=1
        elif event.get_id() == "Collector":
            c_id = binding[0][1].value
            #print(c_id)
            self.complete_times[c_id] = time
            for i in range(int(time),SIMULATION_DURATION):
                self.time_num_token_in_workflow[i]-=1
            #print("COMPLETED "+c_id)
        elif event.get_id() == "Timer":
            #print("---:", workflow.places )
            for p in workflow.places:
                if p.get_id().endswith("_p") and not p.get_id().startswith("Timer"):
                    #print("p:",len(p.marking))
                    length = self.wait_length_x_task.get(p.get_id(),0)
                    for t in p.marking:
                        #print("----t:",t.time,time)
                        if t.time < time:
                            length = length + 1
                    self.wait_length_x_task[p.get_id()] = length
                    #print("---",p.get_id(),length)
            #print("---",len(binding[0][0].marking))
        else:
            waiting_wf=self.wait_time_x_workflow.get(binding[0][1].value, 0)
            waiting_wf=waiting_wf+(time-binding[0][1].time)
            self.wait_time_x_workflow[binding[0][1].value]=waiting_wf

            waiting_tsk=self.wait_time_x_task.get(binding[0][0]._id, 0)
            waiting_tsk=waiting_tsk+(time-binding[0][1].time)
            self.wait_time_x_task[binding[0][0]._id]=waiting_tsk



    def mean_cycle_time(self):
        num_completed=len(self.complete_times.keys())
        #print(num_completed)
        mean_cycle_time=0
        for c_id in self.complete_times.keys():
            mean_cycle_time=mean_cycle_time+(self.complete_times[c_id]-self.arrival_times[c_id])/num_completed
        return mean_cycle_time

    def mean_system_load(self):
        mean_throughput=0
        for elem in self.time_num_token_in_workflow:
            mean_throughput+=elem
        return mean_throughput / len(self.time_num_token_in_workflow)

def mean_requestUtilizationTimeTaskSeq():
    mean = 0
    count = 0
    for key in requestUtilizationTimeTaskSeq:
        mean += requestUtilizationTimeTaskSeq[key]
        count += 1
    return mean/count

##### VISUALISATION
from insidervisualization import Visualisation
layoutWF = "./Layout/BeltWasteRecyclingV1_parser.txt"
v = Visualisation(workflow, layoutWF)
v.show("BeltWasteRecyclingV1_parser")
v.save_layout(layoutWF)


####SIMULAZIONE
# Run the simulation.
reporter=InsiderReporter()
workflow.simulate(SIMULATION_DURATION, reporter)

#### IMAGE wait_time_x_workflow
x_wait_time_x_workflow = []
y_wait_time_x_workflow = []
xticks = []
count = 0
for key in reporter.wait_time_x_workflow.keys():
    if key.startswith(name_token):
        try:
            x_wait_time_x_workflow.append(key)
            y_wait_time_x_workflow.append( round(reporter.wait_time_x_workflow[key],10) )
            if count % 20 == 0:
                xticks.append(key)
            count = count + 1
        except:
            print("except:",key)

plt.close()
plt.figure(figsize=(15,10))
plt.plot(x_wait_time_x_workflow, y_wait_time_x_workflow, color="blue")
plt.xlabel("Request")
plt.xticks(xticks,rotation=45)
plt.ylabel("wait_time")
plt.savefig("./images/BeltWasteRecyclingV1_parser_wait_time_x_workflow.png")


#### IMAGE wait_time_x_task
x_wait_time_x_task = []
y_wait_time_x_task = []
for key in reporter.wait_time_x_task.keys():
    try:
        x_wait_time_x_task.append(key)
        y_wait_time_x_task.append( round(reporter.wait_time_x_task[key],10) )
    except:
        print("except:",key)

plt.close()
plt.figure(figsize=(15,10))
plt.bar(x_wait_time_x_task, y_wait_time_x_task, color="blue")
plt.xlabel("Task")
plt.xticks(rotation=45)
plt.ylabel("Wait time")
plt.savefig("./images/BeltWasteRecyclingV1_parser_wait_time_x_task.png")

#### IMAGE wait_length_x_task
print("-----",reporter.wait_length_x_task)
x_wait_length_x_task = []
y_wait_length_x_task = []
for key in reporter.wait_length_x_task.keys():
    try:
        x_wait_length_x_task.append(key)
        y_wait_length_x_task.append( round(reporter.wait_length_x_task[key]/SIMULATION_DURATION,10) )
    except:
        print("except:",key)

plt.close()
plt.figure(figsize=(15,10))
plt.bar(x_wait_length_x_task, y_wait_length_x_task, color="blue")
plt.xlabel("Task")
plt.xticks(rotation=45)
plt.ylabel("Wait length")
plt.savefig("./images/BeltWasteRecyclingV1_parser_wait_length_x_task.png")

#### IMAGE cycle_time
x_complete_times = []
y_complete_times = []
xticks = []
count = 0
for key in reporter.complete_times.keys():
    if key.startswith(name_token):
        try:
            y_complete_times.append(round(reporter.complete_times[key]-reporter.arrival_times[key],10))
            x_complete_times.append(key)
            if count % 20 == 0:
                xticks.append(key)
            count = count + 1
        except:
            print("except:",key)

plt.close()
plt.figure(figsize=(15,10))
plt.plot(x_complete_times, y_complete_times, color="blue")
plt.xlabel("Request")
plt.xticks(xticks,rotation=45)
plt.ylabel("cycle_time")
plt.savefig("./images/BeltWasteRecyclingV1_parser_cycle_time.png")


#### IMAGE system_load
x_time_nume_token= range(0, SIMULATION_DURATION)
y_time_nume_token= reporter.time_num_token_in_workflow

plt.close()
plt.figure(figsize=(15,10))
plt.plot(x_time_nume_token, y_time_nume_token, color="blue")
plt.xlabel("Time")
plt.xticks(rotation=45)
plt.ylabel("System load")
plt.savefig("./images/BeltWasteRecyclingV1_parser_system_load.png")


#### IMAGE RHO
rhoCount = collections.OrderedDict(sorted(rhoCount.items())) # ordino per raggruppare per tipo di task
x_rho = []
y_rho = []
for key in rhoCount:
    x_rho.append(key)
    y_rho.append(round(rhoCount[key]/SIMULATION_DURATION,10))

plt.close()
plt.figure(figsize=(8,5))
plt.bar(x_rho, y_rho, color="blue")
plt.xlabel("Task")
plt.xticks(rotation=45)
plt.yticks(np. arange(0, 1.1, step=0.2))
plt.ylabel("RHO")
plt.savefig("./images/BeltWasteRecyclingV1_parser_RHO.png")


#### IMAGE ResourceUtilization
resourceUtilizationTime = collections.OrderedDict(sorted(resourceUtilizationTime.items()))
x_ResourceUtilization = []
y_ResourceUtilization = []
for key in resourceUtilizationTime:
    x_ResourceUtilization.append(key)
    y_ResourceUtilization.append(round(resourceUtilizationTime[key]/SIMULATION_DURATION,10))

plt.close()
plt.figure(figsize=(8,5))
plt.bar(x_ResourceUtilization, y_ResourceUtilization, color="blue")
plt.xlabel("Resource")
plt.xticks(rotation=45)
plt.yticks(np. arange(0, 1.1, step=0.2))
plt.ylabel("RHO")
plt.savefig("./images/BeltWasteRecyclingV1_parser_ResourceUtilization.png")

#### PRINT medie valori
print("mean_cycle_time:",reporter.mean_cycle_time())
print("mean_system_load:", reporter.mean_system_load())
print("mean_task_sequence_time:", mean_requestUtilizationTimeTaskSeq())

