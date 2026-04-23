import collections
import matplotlib.pyplot as plt
import numpy as np
from simpn.simulator import SimProblem
from simpn.simulator import SimToken
from simpn.reporters import Reporter

from WorkflowManager import WorkflowManager


######## PARAMETRI SIMULATORE ##################################################################
class InsiderSimulator:
    def __init__(self, name_token="Req_",inputAverageArrivalTime=2.0,SIMULATION_DURATION=1*10*60,name="SimulatioName"):
        self.name_token = name_token#"Req_"
        #self.Tasks = []
        self.name = name

        self.inputAverageArrivalTime = inputAverageArrivalTime# 2.0 # secondi
        self.SIMULATION_DURATION = SIMULATION_DURATION #1*10*60 # secondi = ore*minuti*secondi
        self.rhoCount = dict()
        self.resourceUtilizationTime=dict()
        self.requestUtilizationTimeTaskSeq=dict()

        self.input_path = None
        self.dictAllocation = None
        self.dictResources = None
        self.dictTasks = None
        self.jsonWorkflow = None
        self.allocationHash = ""
        self.simResult = None
        self.workflowCost = -1
        self.zfillLen = 0


    def visualize_sim(self,workflow, input_path="../../layout/BeltWasteRecyclingV1_parser.txt",image_path="pippo"):
        #### VISUALISATION
        from src.Insider.insidervisualization import Visualisation
        layoutWF=input_path+"Layout.txt"
        v = Visualisation(workflow, layoutWF)
        #print("image_path:",image_path)
        v.show(image_path+self.name+"_PetriNet.png")
        v.save_layout(layoutWF)

    def run(self,workflow,reporter=None):
        if reporter is None:
            self.reporter = InsiderReporter(insider_simulator=self,workflow=workflow)
        else:
            self.reporter=reporter
        workflow.simulate(self.SIMULATION_DURATION, self.reporter)
        dataRep = self.reporter.get_metrics()
        #print(dataRep)
        self.simResult = dataRep
        #InsiderUtil.setJsonKeyValues(self.input_path+'sim_result.json',dataRep)

    def getServiceTime(self,nameTask, dictTasks):
        #print("nameTask:",nameTask)
        #print(dictTasks)
        #print(dictTasks[nameTask])
        duration = np.random.exponential(self.getAvgServiceTime(nameTask, dictTasks))
        #duration = self.getAvgServiceTime(nameTask, dictTasks)/3
        return duration

    def getAvgServiceTime(self,nameTask, dictTasks):
        task = dictTasks.get(nameTask)

        if task.type == 0:
            beta = task.requestMilionsOfInstructions / task.executor.MIPS
            return beta
        elif task.type == 1:
            beta = task.requestTransferMB / task.executor.uploadSpeed
            return beta
        elif task.type == 2:
            beta = task.requestStoreMB / task.executor.querySpeedWrite
            return beta
        else:
            raise ValueError("Task type not recognized")


    def updaterRhoCount(self, nameTask, duration):
        if nameTask in self.rhoCount:
            self.rhoCount[nameTask] = self.rhoCount[nameTask] + duration
        else:
            self.rhoCount[nameTask] = duration

    def updateReourceUtilizationTime(self, nameToken, duration):
        if nameToken in self.resourceUtilizationTime:
            # se la richiesta già esiste aggiungo la duration corrente al totale
            self.resourceUtilizationTime[nameToken] = self.resourceUtilizationTime[nameToken] + duration
        else:
            # alrimenti creo la richiesta e gli setto la duration corrente
            self.resourceUtilizationTime[nameToken] = duration


    def updaterRequestUtilizationTimeTaskSeq(self,nameToken, duration):
        if nameToken in self.requestUtilizationTimeTaskSeq:
            # se la richiesta già esiste aggiungo la duration corrente al totale
            self.requestUtilizationTimeTaskSeq[nameToken] = self.requestUtilizationTimeTaskSeq[nameToken] + duration
        else:
            # alrimenti creo la richiesta e gli setto la duration corrente
            self.requestUtilizationTimeTaskSeq[nameToken] = duration


######### Read data from file ##################################################################
class InsiderParser:

    def __init__(self,insider_simulator):
        self.insider_simulator=insider_simulator
        self.name_token=insider_simulator.name_token

    def getTaskString(self, inttype):
        if inttype == 0:
            return "COMPUTE"
        elif inttype == 1:
            return "NETWORK"
        elif inttype == 2:
            return "STORAGE"
        else:
            raise ValueError("Task type not recognized")

    def getTaskType(tt):
        if "Tc".lower() == tt.lower():
            return 0
        elif "Tn".lower() == tt.lower():
            return 1
        elif "Ts".lower() == tt.lower():
            return 2
        else:
            raise ValueError("Task type not recognized")

    def parse(self):

        allocation = []
        for key in self.insider_simulator.dictAllocation:
            line = []
            line.append(key)
            for elem in self.insider_simulator.dictAllocation[key]:
                line.append(elem)
            allocation.append(line)

        #print("allocation:",allocation)

        for keyT in self.insider_simulator.dictTasks:
            for elemAllocationRow in allocation:
                for elem in elemAllocationRow:
                    if self.insider_simulator.dictTasks[keyT].name == elem:
                        #print("check", elemAllocationRow[0],self.dictResources[elemAllocationRow[0]] )
                        #print(elemTask.executor)
                        self.insider_simulator.dictTasks[keyT].executor = self.insider_simulator.dictResources[elemAllocationRow[0]]

        # print allocation
        #for keyT in self.insider_simulator.dictTasks:
        #    print("Task:",self.insider_simulator.dictTasks[keyT].name, " on Resources:", self.insider_simulator.dictTasks[keyT].executor)


        ########## Create workflow ######################################################################

        # Instantiate a simulation problem.
        workflow = SimProblem()

        ######### Timer per statistiche da rimuovere #####################################################
        #Timer_p = WorkflowManager.insider_add_var(workflow, {"name": "Timer_p", "type": ""})
        #Timer_p.put("Timer")
        #def Timer_t(c):
        #    return [SimToken(c, delay=1)]
        #WorkflowManager.insider_add_event(workflow,[Timer_p],[Timer_p], Timer_t,
        #                                  {"name":"Timer","type":""})


        ##########################  PARSER Start #########################################################

        # Dato un ramo identificato da sorgente destinazione,
        # restituisce zero se questo ramo è l'unico in ingresso alla destinazione
        # altrimenti se ci sono più rami in ingresso restituisce la posizione della sorgente nel json
        def getInPositionDestTask(connections,sourceTask,destTask):
            inFlowDest = []
            for connection in connections:
                if connection["dest"] == destTask:
                    inFlowDest.append(connection["source"])
            if len(inFlowDest) == 1:
                return 0
            else:
                return inFlowDest.index(sourceTask)+1


        def getNodeByName(name):
            for node in self.insider_simulator.jsonWorkflow['nodes']:
                if node['nameTask'] == name:
                    return node

        ## dato un task, verifico i posti in ingresso (inflow) e uscita (outflow)
        def getFlow(connections, node, withResources=False):
            inFlow = []
            outFlow = []
            for connection in connections:
                #print("con:",connection["source"],connection["dest"])
                if connection["source"] == node['nameTask']:
                    nodeDest = getNodeByName(connection["dest"])
                    index = getInPositionDestTask(connections, connection["source"], connection["dest"])
                    edgeNumber = ""
                    if index != 0 and nodeDest["flowin"][0]!="join" and index != nodeDest["flowin"][1]!="or":
                        edgeNumber = edgeNumber + str(index)
                    if connection["dest"]+"_p"+edgeNumber not in outFlow:
                        outFlow.append(connection["dest"]+"_p"+edgeNumber)
                if connection["dest"] == node['nameTask']:
                    index = getInPositionDestTask(connections, connection["source"], connection["dest"])
                    edgeNumber = ""
                    if index != 0 and node["flowin"][0]!="join" and index != node["flowin"][1]!="or":
                        edgeNumber = edgeNumber + str(index)
                    if connection["dest"]+"_p"+edgeNumber not in inFlow:
                        inFlow.append(connection["dest"]+"_p"+edgeNumber)

            if withResources:
                #### Per ogni task trovo la risorsa associata e la appendo come ultimo elemento
                #### di inFlow e outFlow
                for row in allocation:
                    for element in row:
                        if element == node['nameTask']:
                            inFlow.append(row[0])
                            outFlow.append(row[0])

            return inFlow, outFlow

        places = {}

        # Aggiungo il place per la sorgente
        placesSourceName = ''
        for node in self.insider_simulator.jsonWorkflow['nodes']:
            if node['type'] == 'BEGIN':
                placesSourceName = node['start']
        auxVar_p = WorkflowManager.insider_add_var(workflow, {"name": placesSourceName ,"type": "BEGIN"})
        places[placesSourceName] = auxVar_p

        # Creo tutti gli altri place
        for node in self.insider_simulator.jsonWorkflow['nodes']:
            type = node['type']
            inFlow, outFlow = getFlow(self.insider_simulator.jsonWorkflow["connections"],node)
            #print(node['nameTask'],inFlow,outFlow)
            for plcs in inFlow:
                if plcs not in places:
                    auxVar_p = WorkflowManager.insider_add_var(workflow, {"name": plcs ,"type": type})
                    places[plcs] = auxVar_p


        ### Creo per ogni risorsa del file Allocation.csv la relativa risorsa
        for resource in allocation:
            # devo prima recuperare il tipo dal primo task asseganto alla risorsa
            inttype = self.insider_simulator.dictTasks[resource[1]].type
            strType = self.getTaskString(inttype)

            auxVar_p = WorkflowManager.insider_add_var(workflow, {"name": resource[0], "type": strType,
                                               "resource": resource[0] })
            places[resource[0]] = auxVar_p

        #print("---places")
        #print(places)

        def getOutFlowPercentage(nameTask):
            total = 0
            res = []
            for connection in self.insider_simulator.jsonWorkflow['connections']:
                if connection["source"] == nameTask:
                    res.append([total,total+connection["probability"]])
                    total = total + connection["probability"]
            return res


        def createTransationFromJsonNode(node):

            inFlow, outFlow = getFlow(self.insider_simulator.jsonWorkflow["connections"], node, withResources=True)

            #print("inout:",inFlow,outFlow)

            if node["type"] == "BEGIN":
                places[node["start"]].put(self.name_token + str(1))
                def myfun(*x,**y):
                    next_token=((int)(x[0].replace(self.insider_simulator.name_token, "")))+1
                    #print(f"now={time.time()},next_token={next_token}")
                    return [SimToken(self.insider_simulator.name_token + str(next_token),
                                     delay=np.random.exponential(self.insider_simulator.inputAverageArrivalTime)), SimToken(x[0], delay=0)]
            elif node["type"] == "END":
                def myfun(*x,**y):
                    return []
            else:
                def myfun(*x,**y):
                    nameTask=node["nameTask"]
                    duration = self.insider_simulator.getServiceTime(node["nameTask"], self.insider_simulator.dictTasks)
                    self.insider_simulator.updaterRhoCount(nameTask, duration)
                    #print(x)
                    self.insider_simulator.updateReourceUtilizationTime( x[len(inFlow)-1], duration)
                    self.insider_simulator.updaterRequestUtilizationTimeTaskSeq(x[0], duration)
                    res=[]
                    #print("-------", nameTask,inFlow,outFlow)
                    percentageList = getOutFlowPercentage(nameTask)
                    #print(percentageList)
                    rnd = np.random.uniform()
                    #print("rnd",rnd)
                    for i in range(len(outFlow)-1):
                        if (node["flowout"][0] == "split" and node["flowout"][1] == "or" and (
                                rnd < percentageList[i][0] or rnd > percentageList[i][1]  ) ):
                            res.append(None)
                        else:
                            res.append(SimToken(x[0],delay=duration))

                    if len(outFlow) >= 1:
                        res.append(SimToken(x[-1],delay=duration))
                    return res

            return myfun


        for node in self.insider_simulator.jsonWorkflow['nodes']:

            myfun=createTransationFromJsonNode(node)
            inFlow, outFlow = getFlow(self.insider_simulator.jsonWorkflow["connections"],node,withResources=True)

            # Aggiungo ramo tra posto sorgente e tansizione sorgente
            if node["type"] == "BEGIN":
                inFlow = [placesSourceName] + inFlow
                outFlow = [placesSourceName] + outFlow

            # guard=lambda c1, c2,c3, c4: c1 == c2 == c3 == c4
            guardF = None
            if node["flowin"][0] == "join" and node["flowin"][1] == "and":
                def tmpfun(*x):
                    t = x[0]
                    for i in range(1,len(x)-1):
                        if x[i] != t:
                            return False
                    return True
                guardF = tmpfun

            # Sistemo la grafica join/split - and/or
            flow = ""
            if node["flowin"][1] != "":
                flow = node["flowin"][1]
            if node["flowout"][1] != "":
                flow = node["flowout"][1]

            inf = []
            for pname in inFlow:
                inf.append(places[pname])
            outf = []
            for pname in outFlow:
                outf.append(places[pname])

            WorkflowManager.insider_add_event(workflow, inf, outf, myfun,
                                              {"name": node["name"], "type": node["type"], "flow":flow }, guard=guardF)

        return workflow

    ##########################  PARSER End ############################################################


#########################################

######### Run simulation ################

## Reporter statistics
#
class InsiderReporter(Reporter):

    def __init__(self,insider_simulator,workflow):
        self.arrival_times = dict()
        self.start_times = dict()
        self.complete_times = dict()

        self.inssim = insider_simulator
        self.workflow = workflow


        #self.total_proc_time = 0
        #self.wait_time_x_workflow= dict()
        #self.wait_time_x_task= dict()
        #self.time_num_token_in_workflow = [0] * self.inssim.SIMULATION_DURATION
        #self.wait_length_x_task = dict()

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
            #for i in range(int(time),self.inssim.SIMULATION_DURATION):
            #    self.time_num_token_in_workflow[i]+=1
        elif event.get_id() == "Collector":
            c_id = binding[0][1].value
            #print(c_id)
            self.complete_times[c_id] = time
            #for i in range(int(time),self.inssim.SIMULATION_DURATION):
            #    self.time_num_token_in_workflow[i]-=1
            #print("COMPLETED "+c_id)
        # elif event.get_id() == "Timer":
        #     #print("---:", workflow.places )
        #     for p in self.workflow.places:
        #         if p.get_id().endswith("_p") and not p.get_id().startswith("Timer"):
        #             #print("p:",len(p.marking))
        #             length = self.wait_length_x_task.get(p.get_id(),0)
        #             for t in p.marking:
        #                 #print("----t:",t.time,time)
        #                 if t.time < time:
        #                     length = length + 1
        #             self.wait_length_x_task[p.get_id()] = length
        #             #print("---",p.get_id(),length)
        #     #print("---",len(binding[0][0].marking))
        # #else:
        #     #waiting_wf=self.wait_time_x_workflow.get(binding[0][1].value, 0)
        #     #waiting_wf=waiting_wf+(time-binding[0][1].time)
        #     #self.wait_time_x_workflow[binding[0][1].value]=waiting_wf
        #
        #     #waiting_tsk=self.wait_time_x_task.get(binding[0][0]._id, 0)
        #     #waiting_tsk=waiting_tsk+(time-binding[0][1].time)
        #     #self.wait_time_x_task[binding[0][0]._id]=waiting_tsk



    def mean_cycle_time(self):
        num_completed=len(self.complete_times.keys())
        #print(num_completed)
        mean_cycle_time=0
        for c_id in self.complete_times.keys():
            mean_cycle_time=mean_cycle_time+(self.complete_times[c_id]-self.arrival_times[c_id])/num_completed
        return mean_cycle_time

    #def mean_system_load(self):
    #    mean_throughput=0
    #    for elem in self.time_num_token_in_workflow:
    #        mean_throughput+=elem
    #    return mean_throughput / len(self.time_num_token_in_workflow)

    def mean_requestUtilizationTimeTaskSeq(self):
        mean = 0
        count = 0
        for key in self.inssim.requestUtilizationTimeTaskSeq:
            mean += self.inssim.requestUtilizationTimeTaskSeq[key]
            count += 1
        return mean/count

    def get_metrics(self):
        metrics={}
        metrics["mean_cycle_time"]=self.mean_cycle_time()
        metrics["mean_work_time"] = self.mean_requestUtilizationTimeTaskSeq()
        #metrics["max_resource_utilization"] = self.mean_requestUtilizationTimeTaskSeq()
        return metrics

class FiguresGenerator:
    @staticmethod
    def TO_BE_DELETED_generate_wait_time_x_workflow(insiderSimulation,fig_prefix):
        #### IMAGE wait_time_x_workflow
        x_wait_time_x_workflow = []
        y_wait_time_x_workflow = []
        xticks = []
        count = 0
        for key in insiderSimulation.reporter.wait_time_x_workflow_TODELETE.keys():
            if key.startswith(insiderSimulation.name_token):
                try:
                    x_wait_time_x_workflow.append(key)
                    y_wait_time_x_workflow.append(round(insiderSimulation.reporter.wait_time_x_workflow_TODELETE[key], 10))
                    if count % 20 == 0:
                        xticks.append(key)
                    count = count + 1
                except:
                    print("except:", key)

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.plot(x_wait_time_x_workflow, y_wait_time_x_workflow, color="blue")
        plt.xlabel("Request")
        plt.xticks(xticks, rotation=45)
        plt.ylabel("wait_time")
        plt.savefig("./images/" + fig_prefix+insiderSimulation.name+"_wait_time_x_workflowV1.png")

    @staticmethod
    def TO_BE_DELETED_generate_wait_time_x_task(insiderSimulation, fig_prefix):
        #### IMAGE wait_time_x_task
        x_wait_time_x_task = []
        y_wait_time_x_task = []
        for key in insiderSimulation.reporter.wait_time_x_task_TODELETE.keys():
            try:
                x_wait_time_x_task.append(key)
                y_wait_time_x_task.append(round(insiderSimulation.reporter.wait_time_x_task_TODELETE[key], 10))
            except:
                print("except:", key)

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.bar(x_wait_time_x_task, y_wait_time_x_task, color="blue")
        plt.xlabel("Task")
        plt.xticks(rotation=45)
        plt.ylabel("Wait time")
        plt.savefig("./images/" + fig_prefix+insiderSimulation.name+"_wait_time_x_taskV1.png")

    @staticmethod
    def TO_BE_DELETED_generate_wait_length_x_task(insiderSimulation, fig_prefix):
        #### IMAGE wait_length_x_task
        #("-----", insiderSimulation.reporter.wait_length_x_task_TODELETE)
        x_wait_length_x_task = []
        y_wait_length_x_task = []
        for key in insiderSimulation.reporter.wait_length_x_task_TODELETE.keys():
            try:
                x_wait_length_x_task.append(key)
                y_wait_length_x_task.append(
                    round(insiderSimulation.reporter.wait_length_x_task_TODELETE[key] / insiderSimulation.SIMULATION_DURATION, 10))
            except:
                print("except:", key)

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.bar(x_wait_length_x_task, y_wait_length_x_task, color="blue")
        plt.xlabel("Task")
        plt.xticks(rotation=45)
        plt.ylabel("Wait length")
        plt.savefig("./images/" + fig_prefix+insiderSimulation.name+"_wait_length_x_taskV1.png")

    @staticmethod
    def generate_req_completed(insiderSimulation, fig_prefix):
        #### IMAGE req_completed
        x_arrival_times = []
        y_num_reqs = []

        count = 0
        for key in insiderSimulation.reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                try:
                    x_arrival_times.append(round(insiderSimulation.reporter.arrival_times[key], 10))
                    y_num_reqs.append(count)
                    count = count + 1
                except:
                    print("except:", key)

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.plot(x_arrival_times, y_num_reqs, color="blue")
        plt.xlabel("time")
        # plt.xticks(xticks,rotation=45)
        plt.ylabel("request number")
        plt.savefig(fig_prefix + insiderSimulation.name+"_arrivals_time.png")

    @staticmethod
    def generate_completed_time(insiderSimulation, fig_prefix):
        #### IMAGE req_arrivals
        x_complete_times = []
        y_num_reqs = []

        count = 0
        for key in insiderSimulation.reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                # try:
                x_complete_times.append(round(insiderSimulation.reporter.complete_times[key], 10))
                y_num_reqs.append(count)
                count = count + 1
                # except:
                #    print("except:", key)

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.plot(x_complete_times, y_num_reqs, color="blue")
        plt.xlabel("time")
        # plt.xticks(xticks,rotation=45)
        plt.ylabel("request number")
        plt.savefig( fig_prefix+insiderSimulation.name+"_completed_time.png")

    @staticmethod
    def generate_req_in_system(insiderSimulation, fig_prefix):
        #### IMAGE requests in the system
        x_complete_times = []
        for key in insiderSimulation.reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                x_complete_times.append(round(insiderSimulation.reporter.complete_times[key], 10))

        x_arrival_times = []
        for key in insiderSimulation.reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                x_arrival_times.append(round(insiderSimulation.reporter.arrival_times[key], 10))

        x_req_times = [0] * (len(x_complete_times) + len(x_arrival_times))
        y_req_number = [0] * (len(x_complete_times) + len(x_arrival_times))
        index_c = 0
        index_a = 0
        while index_a + index_c < len(x_req_times):
            # print(index_a," ",len(x_arrival_times)," ",index_c," ",len(x_complete_times))
            if (index_a < len(x_arrival_times) and x_arrival_times[index_a] < x_complete_times[index_c]):
                x_req_times[index_a + index_c] = x_arrival_times[index_a]
                y_req_number[index_a + index_c] = y_req_number[index_a + index_c - 1] + 1
                index_a = index_a + 1
            elif ((index_a >= len(x_arrival_times)) or (
                    index_c < len(x_complete_times) and x_arrival_times[index_a] >= x_complete_times[index_c])):
                x_req_times[index_a + index_c] = x_complete_times[index_c]
                y_req_number[index_a + index_c] = y_req_number[index_a + index_c - 1] - 1
                index_c = index_c + 1

        y_avg_req_number = [0] * len(y_req_number)
        for index in range(len(y_avg_req_number)):
            y_avg_req_number[index] = np.average(y_req_number[0:(index + 1)])

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.plot(x_req_times, y_req_number, color="blue")
        plt.plot(x_req_times, y_avg_req_number, color="green")
        plt.xlabel("time")
        # plt.xticks(xticks,rotation=45)
        plt.ylabel("request number")
        plt.savefig(fig_prefix+insiderSimulation.name+"_req_in_system.png")

    @staticmethod
    def generate_cycle_time_avg(insiderSimulation, fig_prefix):
        #### IMAGE average cycle_time
        #print("test")
        x_complete_times = []
        y_complete_times = []
        xticks = []
        count = 0

        for key in insiderSimulation.reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                try:
                    y_complete_times.append(round(insiderSimulation.reporter.complete_times[key] - insiderSimulation.reporter.arrival_times[key], 10))
                    x_complete_times.append(key)
                    if count % int(len(insiderSimulation.reporter.complete_times.keys())//5) == 0:
                        xticks.append(key)
                    count = count + 1
                except:
                    print("except:", key)
        y_avg_complete_times = [0] * len(y_complete_times)
        for index in range(len(y_avg_complete_times)):
            y_avg_complete_times[index] = np.average(y_complete_times[0:(index + 1)])

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.plot(x_complete_times, y_avg_complete_times, color="green")
        plt.scatter(x_complete_times, y_complete_times, color="blue")
        plt.xlabel("Request")
        plt.xticks(xticks)#, rotation=45)
        plt.ylabel("cycle_time")
        plt.savefig(fig_prefix+insiderSimulation.name+"_cycle_time_avgV1.png")

    @staticmethod
    def TO_BE_DELETED_generate_system_load(insiderSimulation, fig_prefix):
        #### IMAGE system_load
        x_time_nume_token = range(0, insiderSimulation.SIMULATION_DURATION)
        y_time_nume_token = insiderSimulation.reporter.time_num_token_in_workflow_TODELETE

        plt.close()
        #plt.figure(figsize=(15, 10))
        plt.plot(x_time_nume_token, y_time_nume_token, color="blue")
        plt.xlabel("Time")
        plt.xticks(rotation=45)
        plt.ylabel("System load")
        plt.savefig("./images/" + fig_prefix+insiderSimulation.name+"_system_loadV1.png")

    @staticmethod
    def generate_rho(insiderSimulation, fig_prefix):
        #### IMAGE RHO
        rhoCount = collections.OrderedDict(sorted(insiderSimulation.rhoCount.items())) # ordino per raggruppare per tipo di task
        x_rho = []
        y_rho = []
        for key in rhoCount:
            x_rho.append(key)
            y_rho.append(round(rhoCount[key]/insiderSimulation.SIMULATION_DURATION,10))

        plt.close()
        #plt.figure(figsize=(8,5))
        plt.bar(x_rho, y_rho, color="blue")
        plt.xlabel("Task")
        plt.xticks(rotation=45)
        plt.yticks(np. arange(0, 1.1, step=0.2))
        plt.ylabel("RHO")
        plt.savefig(fig_prefix+insiderSimulation.name+"_RHOV1.png")

    @staticmethod
    def generate_resource_utilization(insiderSimulation, fig_prefix):
        #### IMAGE ResourceUtilization
        #print(insiderSimulation.resourceUtilizationTime)
        #print(insiderSimulation.resourceUtilizationTime.items())
        #print(sorted(insiderSimulation.resourceUtilizationTime.items()))
        resourceUtilizationTime = collections.OrderedDict(sorted([(str(key),value)for key,value in insiderSimulation.resourceUtilizationTime.items()]))
        x_ResourceUtilization = []
        y_ResourceUtilization = []
        for key in resourceUtilizationTime:
            x_ResourceUtilization.append(key)
            y_ResourceUtilization.append(round(resourceUtilizationTime[key]/insiderSimulation.SIMULATION_DURATION,10))

        plt.close()
        #plt.figure(figsize=(8,5))
        plt.bar(x_ResourceUtilization, y_ResourceUtilization, color="blue")
        plt.xlabel("Resource")
        plt.xticks(rotation=45)
        plt.yticks(np. arange(0, 1.1, step=0.2))
        plt.ylabel("RHO")
        plt.savefig(fig_prefix+insiderSimulation.name+"_ResourceUtilizationV1.png")

    @staticmethod
    def generate_figures(insiderSimulation,fig_prefix):
        FiguresGenerator.generate_req_completed(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_completed_time(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_req_in_system(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_cycle_time_avg(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_rho(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_resource_utilization(insiderSimulation, fig_prefix)
        # FiguresGenerator.generate_wait_time_x_workflow(insiderSimulation, fig_prefix)
        # FiguresGenerator.generate_wait_time_x_task(insiderSimulation, fig_prefix)
        # FiguresGenerator.generate_wait_length_x_task(insiderSimulation, fig_prefix)
        #FiguresGenerator.generate_system_load(insiderSimulation, fig_prefix)



