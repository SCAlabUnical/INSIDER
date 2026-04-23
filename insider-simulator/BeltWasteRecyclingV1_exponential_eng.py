import collections
import random
import time

import matplotlib.pyplot as plt
import numpy as np
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp
from simpn.reporters import Reporter, SimpleReporter

from BeltWasteRecyclingV1_exponential import x_complete_times
from InsiderSimulation import InsiderSimulator
from WorkflowManager import WorkflowManager
from Resource import Node
from Task import Task
import csv
    

######## PARAMETRI SIMULATORE ###########


#########################################


######## Funzioni di utilità ############

#########################################

######### Read data from file ###########

# Importazione dei dati delle risorse da file
class Importer:
    @staticmethod
    def import_from_files(insiderSimulator):
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

                auxTask = Task(spamreader.line_num-1,insiderSimulator.getTasktype(row[0]))

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
            print("Task:",element.name, " on Resources:", element.executor.__dict__, "with average duration: ")

        dictTasks= {}
        for item in Tasks:
            dictTasks[item.name]=item
        print("---")
        print(dictTasks)
        print("---")

        return dictTasks

    @staticmethod
    def build_workflow(insiderSimulator):
########## Create workflow ##############
        dictTasks=Importer.import_from_files(insiderSimulator)
# Instantiate a simulation problem.
        workflow = SimProblem()

        Timer_p = WorkflowManager.insider_add_var(workflow, {"name": "Timer_p", "type": ""})

        # Define queues and other 'places' in the process.
        Tn0_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn0_p", "type": ""})
        Tn1_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn1_p", "type": "NETWORK"})
        Tn2_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn2_p", "type": "NETWORK"})
        Tn3_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn3_p", "type": "NETWORK"})
        Tn4_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn4_p", "type": "NETWORK"})
        Tn5_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn5_p", "type": "NETWORK"})
        Tn6_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_p", "type": "NETWORK"})
        Tn7_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn7_p", "type": "NETWORK"})
        Tn8_p1 = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_p1", "type": ""})
        Tn8_p2 = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_p2", "type": ""})
        Tn8_p3 = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_p3", "type": ""})
        Tn8_p4 = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_p4", "type": ""})
        Tc1_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc1_p", "type": "COMPUTE"})
        Tc2_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_p", "type": "COMPUTE"})
        Tc3_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_p", "type": "COMPUTE"})
        Tc4_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc4_p", "type": "COMPUTE"})
        Tc5_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc5_p", "type": "COMPUTE"})
        Ts1_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts1_p", "type": "STORAGE"})
        Ts2_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts2_p", "type": "STORAGE"})
        Ts3_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts3_p", "type": "STORAGE"})

        # Define a 'places' with resources.
        #Tn0_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn0_r", "type": "", "resource": "n0_r"})
        Tn1_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn1_r", "type": "NETWORK", "resource": "n1_r"})
        Tn2_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn2_r", "type": "NETWORK", "resource": "n2_r"})
        Tn3_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn3_r", "type": "NETWORK", "resource": "n3_r"})
        Tn4_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn4_r", "type": "NETWORK", "resource": "n4_r"})
        Tn5_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn5_r", "type": "NETWORK", "resource": "n5_r"})
        Tn6_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_r", "type": "NETWORK", "resource": "n6_r"})
        Tn7_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn7_r", "type": "NETWORK", "resource": "n7_r"})
        #Tn8_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_r", "type": "", "resource": "n8_r"})
        Tc1_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc1_r", "type": "COMPUTE", "resource": "c1_r"})
        #Tc2_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_r", "type": "COMPUTE", "resource": "c2_r"})
        #Tc1_r.put("c2_r")
        Tc3_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_r", "type": "COMPUTE", "resource": "c3_r"})
        #Tc4_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc4_r", "type": "COMPUTE", "resource": "c4_r"})
        #Tc3_r.put("c4_r")
        Tc5_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc5_r", "type": "COMPUTE", "resource": "c5_r"})
        Ts1_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts1_r", "type": "STORAGE", "resource": "s1_r"})
        #Ts2_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts2_r", "type": "STORAGE", "resource": "s2_r"})
        #Ts1_r.put("s2_r")
        #Ts3_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts3_r", "type": "STORAGE", "resource": "s3_r"})
        #Ts1_r.put("s3_r")


        #Timer_p.put("Timer")

        #def Timer_t(c):
        #    return [SimToken(c, delay=1)]
        #WorkflowManager.insider_add_event(workflow,[Timer_p],[Timer_p], Timer_t,
        #                                  {"name":"Timer","type":""})

        # Define events.
        # Tn Task network
        #curr_token=1
        Tn0_p.put(insiderSimulator.name_token + str(1))

        def Tc0_t(c):
            next_token=((int)(c.replace(insiderSimulator.name_token, "")))+1
            print(f"now={time.time()},next_token={next_token}")
            return [SimToken(insiderSimulator.name_token+str(next_token), delay=np.random.exponential(insiderSimulator.inputAverageArrivalTime)),
                    SimToken(c, delay=0)]
        WorkflowManager.insider_add_event(workflow,[Tn0_p],[Tn0_p,Tc1_p], Tc0_t,
                                          {"name":"Source","type":""})

        def Tc1_t(c,r):
            nameTask="Tc1"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c,duration)

            return [ SimToken(c, delay=duration), SimToken(c, delay=duration), SimToken(r, delay=duration) ]
        WorkflowManager.insider_add_event(workflow,[Tc1_p, Tc1_r],[ Tn1_p, Tn5_p, Tc1_r], Tc1_t,
                                          {"name":"Camera_acquisition","type":"COMPUTE","flow":"And"})

        def Tn1_t(c,r):
            nameTask = "Tn1"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c,duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow, [Tn1_p, Tn1_r], [Tc2_p, Tn1_r], Tn1_t,
                                          {"name":"Tn1_t","type":"NETWORK"})

        def Tc2_t(c,r):
            nameTask = "Tc2"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r,delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tc2_p, Tc1_r], [Tn2_p, Tc1_r], Tc2_t,
                                          {"name":"Image processing","type":"COMPUTE"})

        def Tn2_t(c,r):
            nameTask = "Tn2"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow, [Tn2_p, Tn2_r],[Tc3_p, Tn2_r], Tn2_t,
                                          {"name":"Tn2_t","type":"NETWORK"})

        def Tc3_t(c,r):
            nameTask = "Tc3"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tc3_p, Tc3_r], [Tn3_p, Tn6_p, Tc3_r], Tc3_t,
                                          {"name":"Segmentation","type":"COMPUTE","flow":"And"})

        def Tn3_t(c,r):
            nameTask = "Tn3"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow, [Tn3_p, Tn3_r], [Tc4_p, Tn3_r], Tn3_t,
                                          {"name":"Tn3_t","type":"NETWORK"})

        def Tc4_t(c,r):
            nameTask = "Tc4"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tc4_p, Tc3_r], [Tn4_p, Tn7_p, Tc3_r], Tc4_t,
                                          {"name":"Belt command","type":"COMPUTE","flow":"And"})

        def Tn4_t(c,r):
            nameTask = "Tn4"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tn4_p, Tn4_r], [Tc5_p, Tn4_r], Tn4_t,
                                          {"name":"Tn4_t","type":"NETWORK"})

        def Tc5_t(c,r):
            nameTask = "Tc5"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tc5_p, Tc5_r], [Tn8_p1,Tc5_r], Tc5_t,
                                          {"name":"Actuator","type":"COMPUTE"})

        def Tn5_t(c,r):
            nameTask = "Tn5"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            #insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tn5_p, Tn5_r], [Ts1_p, Tn5_r], Tn5_t,
                                          {"name":"Tn5_t","type":"NETWORK"})

        def Ts1_t(c,r):
            nameTask = "Ts1"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            # insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow, [Ts1_p, Ts1_r], [Tn8_p2, Ts1_r], Ts1_t,
                                          {"name":"Ts1_t","type":"STORAGE"})

        def Tn6_t(c,r):
            nameTask = "Tn6"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            # insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tn6_p, Tn6_r], [Ts2_p, Tn6_r], Tn6_t,
                                          {"name":"Tn6_t","type":"NETWORK"})

        def Ts2_t(c,r):
            nameTask = "Ts2"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            # insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow, [Ts2_p, Ts1_r], [Tn8_p3,Ts1_r], Ts2_t,
                                          {"name":"Ts2_t","type":"STORAGE"})

        def Tn7_t(c,r):
            nameTask = "Tn7"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            # insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration), SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow,[Tn7_p, Tn7_r], [Ts3_p, Tn7_r], Tn7_t,
                                          {"name":"Tn7_t","type":"NETWORK"})

        def Ts3_t(c,r):
            nameTask = "Ts3"
            duration = insiderSimulator.getServiceTime(nameTask, dictTasks)
            insiderSimulator.updaterRhoCount(nameTask, duration)
            insiderSimulator.updateReourceUtilizationTime(r, duration)
            # insiderSimulator.updaterRequestUtilizationTimeTaskSeq(c, duration)
            return [SimToken(c, delay=duration),SimToken(r, delay=duration)]
        WorkflowManager.insider_add_event(workflow, [Ts3_p, Ts1_r], [Tn8_p4, Ts1_r], Ts3_t,
                                          {"name":"Ts3_t","type":"STORAGE"})


        def Tn8_t(c1, c2, c3 , c4):
            #duration = getServiceTime("Tn8", c1, dictTasks)
            #updateReourceUtilizationTime(r, duration)
            print(f"now={time.time()},completed={c1}")
            return []
        WorkflowManager.insider_add_event(workflow,[Tn8_p1,Tn8_p2,Tn8_p3,Tn8_p4], [], Tn8_t,
                                          {"name":"Collector","type":"","flow":"And"} , guard=lambda c1, c2,c3, c4: c1 == c2 == c3 == c4)

        return workflow
#########################################

######### Run simulation ################

## Reporter statistics
#
class InsiderReporter(Reporter):

    def __init__(self,insiderSimulator,workflow):

        self.arrival_times = dict()
        self.start_times = dict()
        self.complete_times = dict()
        #self.total_proc_time = 0
        self.wait_time_x_workflow_TODELETE= dict()
        self.wait_time_x_task_TODELETE= dict()
        self.time_num_token_in_workflow_TODELETE = [0] * insiderSimulator.SIMULATION_DURATION
        self.wait_length_x_task_TODELETE = dict()

        self.insiderSimulator = insiderSimulator
        self.workflow = workflow

    def callback(self, timed_binding):
        (binding, time, event) = timed_binding
        #print("-------",binding,"-------", time,"-------", event)
        #------- [(Tc2_p, Req_248@494.6790849603186), (Tc1_r, c1_r@494.5977657826795)] ------- 494.6790849603186 ------- Image processing
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
            #for i in range(int(time),SIMULATION_DURATION):
            #    self.time_num_token_in_workflow[i]+=1
        elif event.get_id() == "Collector":
            c_id = binding[0][1].value
            #print(c_id)
            self.complete_times[c_id] = time
            #for i in range(int(time),SIMULATION_DURATION):
            #    self.time_num_token_in_workflow[i]-=1
            #print("COMPLETED "+c_id)
        elif event.get_id() == "Timer":
            #print("---:", workflow.places )
            for p in self.workflow.places:
                if p.get_id().endswith("_p") and not p.get_id().startswith("Timer"):
                    #print("p:",len(p.marking))
                    length = self.wait_length_x_task_TODELETE.get(p.get_id(), 0)
                    for t in p.marking:
                        #print("----t:",t.time,time)
                        if t.time < time:
                            length = length + 1
                    self.wait_length_x_task_TODELETE[p.get_id()] = length
                    #print("---",p.get_id(),length)
            #print("---",len(binding[0][0].marking))
        else:
            waiting_wf=self.wait_time_x_workflow_TODELETE.get(binding[0][1].value, 0)
            waiting_wf=waiting_wf+(time-binding[0][1].time)
            self.wait_time_x_workflow_TODELETE[binding[0][1].value]=waiting_wf

            waiting_tsk=self.wait_time_x_task_TODELETE.get(binding[0][0]._id, 0)
            waiting_tsk=waiting_tsk+(time-binding[0][1].time)
            self.wait_time_x_task_TODELETE[binding[0][0]._id]=waiting_tsk



    def mean_cycle_time(self):
        num_completed=len(self.complete_times.keys())
        #print(num_completed)
        mean_cycle_time=0
        for c_id in self.complete_times.keys():
            mean_cycle_time=mean_cycle_time+(self.complete_times[c_id]-self.arrival_times[c_id])/num_completed
        return mean_cycle_time

    def mean_system_load(self):
        mean_throughput=0
        for elem in self.time_num_token_in_workflow_TODELETE:
            mean_throughput+=elem
        return mean_throughput / len(self.time_num_token_in_workflow_TODELETE)

    def mean_requestUtilizationTimeTaskSeq(self):
        mean = 0
        count = 0
        for key in insiderSimulator.requestUtilizationTimeTaskSeq:
            mean += insiderSimulator.requestUtilizationTimeTaskSeq[key]
            count += 1
        return mean/count


class FiguresGenerator:
    @staticmethod
    def generate_wait_time_x_workflow(insiderSimulation,fig_prefix):
        #### IMAGE wait_time_x_workflow
        x_wait_time_x_workflow = []
        y_wait_time_x_workflow = []
        xticks = []
        count = 0
        for key in reporter.wait_time_x_workflow_TODELETE.keys():
            if key.startswith(insiderSimulation.name_token):
                try:
                    x_wait_time_x_workflow.append(key)
                    y_wait_time_x_workflow.append(round(reporter.wait_time_x_workflow_TODELETE[key], 10))
                    if count % 20 == 0:
                        xticks.append(key)
                    count = count + 1
                except:
                    print("except:", key)

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.plot(x_wait_time_x_workflow, y_wait_time_x_workflow, color="blue")
        plt.xlabel("Request")
        plt.xticks(xticks, rotation=45)
        plt.ylabel("wait_time")
        plt.savefig("./images/" + fig_prefix + "_wait_time_x_workflowV1.png")

    @staticmethod
    def generate_wait_time_x_task(insiderSimulation, fig_prefix):
        #### IMAGE wait_time_x_task
        x_wait_time_x_task = []
        y_wait_time_x_task = []
        for key in reporter.wait_time_x_task_TODELETE.keys():
            try:
                x_wait_time_x_task.append(key)
                y_wait_time_x_task.append(round(reporter.wait_time_x_task_TODELETE[key], 10))
            except:
                print("except:", key)

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.bar(x_wait_time_x_task, y_wait_time_x_task, color="blue")
        plt.xlabel("Task")
        plt.xticks(rotation=45)
        plt.ylabel("Wait time")
        plt.savefig("./images/" + fig_prefix + "_wait_time_x_taskV1.png")

    @staticmethod
    def generate_wait_length_x_task(insiderSimulation, fig_prefix):
        #### IMAGE wait_length_x_task
        print("-----", reporter.wait_length_x_task_TODELETE)
        x_wait_length_x_task = []
        y_wait_length_x_task = []
        for key in reporter.wait_length_x_task_TODELETE.keys():
            try:
                x_wait_length_x_task.append(key)
                y_wait_length_x_task.append(
                    round(reporter.wait_length_x_task_TODELETE[key] / insiderSimulator.SIMULATION_DURATION, 10))
            except:
                print("except:", key)

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.bar(x_wait_length_x_task, y_wait_length_x_task, color="blue")
        plt.xlabel("Task")
        plt.xticks(rotation=45)
        plt.ylabel("Wait length")
        plt.savefig("./images/" + fig_prefix + "_wait_length_x_taskV1.png")

    @staticmethod
    def generate_req_completed(insiderSimulation, fig_prefix):
        #### IMAGE req_completed
        x_arrival_times = []
        y_num_reqs = []

        count = 0
        for key in reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                try:
                    x_arrival_times.append(round(reporter.arrival_times[key], 10))
                    y_num_reqs.append(count)
                    count = count + 1
                except:
                    print("except:", key)

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.plot(x_arrival_times, y_num_reqs, color="blue")
        plt.xlabel("time")
        # plt.xticks(xticks,rotation=45)
        plt.ylabel("request number")
        plt.savefig("./images/" + fig_prefix + "_arrivals_time.png")

    @staticmethod
    def generate_completed_time(insiderSimulation, fig_prefix):
        #### IMAGE req_arrivals
        x_complete_times = []
        y_num_reqs = []

        count = 0
        for key in reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                # try:
                x_complete_times.append(round(reporter.complete_times[key], 10))
                y_num_reqs.append(count)
                count = count + 1
                # except:
                #    print("except:", key)

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.plot(x_complete_times, y_num_reqs, color="blue")
        plt.xlabel("time")
        # plt.xticks(xticks,rotation=45)
        plt.ylabel("request number")
        plt.savefig("./images/" + fig_prefix + "_completed_time.png")

    @staticmethod
    def generate_req_in_system(insiderSimulation, fig_prefix):
        #### IMAGE requests in the system
        x_complete_times = []
        for key in reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                x_complete_times.append(round(reporter.complete_times[key], 10))

        x_arrival_times = []
        for key in reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                x_arrival_times.append(round(reporter.arrival_times[key], 10))

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
        plt.figure(figsize=(15, 10))
        plt.plot(x_req_times, y_req_number, color="blue")
        plt.plot(x_req_times, y_avg_req_number, color="green")
        plt.xlabel("time")
        # plt.xticks(xticks,rotation=45)
        plt.ylabel("request number")
        plt.savefig("./images/" + fig_prefix + "_req_in_system.png")

    @staticmethod
    def generate_cycle_time_avg(insiderSimulation, fig_prefix):
        #### IMAGE average cycle_time
        print("test")
        x_complete_times = []
        y_complete_times = []
        xticks = []
        count = 0

        for key in reporter.complete_times.keys():
            if key.startswith(insiderSimulation.name_token):
                try:
                    y_complete_times.append(round(reporter.complete_times[key] - reporter.arrival_times[key], 10))
                    x_complete_times.append(key)
                    if count % 20 == 0:
                        xticks.append(key)
                    count = count + 1
                except:
                    print("except:", key)
        y_avg_complete_times = [0] * len(y_complete_times)
        for index in range(len(y_avg_complete_times)):
            y_avg_complete_times[index] = np.average(y_complete_times[0:(index + 1)])

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.plot(x_complete_times, y_avg_complete_times, color="green")
        plt.plot(x_complete_times, y_complete_times, color="blue")
        plt.xlabel("Request")
        plt.xticks(xticks, rotation=45)
        plt.ylabel("cycle_time")
        plt.savefig("./images/" + fig_prefix + "_cycle_time_avgV1.png")

    @staticmethod
    def generate_system_load(insiderSimulation, fig_prefix):
        #### IMAGE system_load
        x_time_nume_token = range(0, insiderSimulation.SIMULATION_DURATION)
        y_time_nume_token = reporter.time_num_token_in_workflow_TODELETE

        plt.close()
        plt.figure(figsize=(15, 10))
        plt.plot(x_time_nume_token, y_time_nume_token, color="blue")
        plt.xlabel("Time")
        plt.xticks(rotation=45)
        plt.ylabel("System load")
        plt.savefig("./images/" + fig_prefix + "_system_loadV1.png")

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
        plt.figure(figsize=(8,5))
        plt.bar(x_rho, y_rho, color="blue")
        plt.xlabel("Task")
        plt.xticks(rotation=45)
        plt.yticks(np. arange(0, 1.1, step=0.2))
        plt.ylabel("RHO")
        plt.savefig("./images/"+fig_prefix+"_RHOV1.png")

    @staticmethod
    def generate_resource_utilization(insiderSimulation, fig_prefix):
        #### IMAGE ResourceUtilization
        resourceUtilizationTime = collections.OrderedDict(sorted(insiderSimulation.resourceUtilizationTime.items()))
        x_ResourceUtilization = []
        y_ResourceUtilization = []
        for key in resourceUtilizationTime:
            x_ResourceUtilization.append(key)
            y_ResourceUtilization.append(round(resourceUtilizationTime[key]/insiderSimulation.SIMULATION_DURATION,10))

        plt.close()
        plt.figure(figsize=(8,5))
        plt.bar(x_ResourceUtilization, y_ResourceUtilization, color="blue")
        plt.xlabel("Resource")
        plt.xticks(rotation=45)
        plt.yticks(np. arange(0, 1.1, step=0.2))
        plt.ylabel("RHO")
        plt.savefig("./images/"+fig_prefix+"_ResourceUtilizationV1.png")

    @staticmethod
    def generate_figures(insiderSimulation,fig_prefix):
        FiguresGenerator.generate_wait_time_x_workflow(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_wait_time_x_task(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_wait_length_x_task(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_req_completed(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_completed_time(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_req_in_system(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_cycle_time_avg(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_system_load(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_rho(insiderSimulation, fig_prefix)
        FiguresGenerator.generate_resource_utilization(insiderSimulation, fig_prefix)





















if __name__ == '__main__':

    insiderSimulator = InsiderSimulator(inputAverageArrivalTime=2.5, SIMULATION_DURATION=10 * 10 * 60)
    workflow=Importer.build_workflow(insiderSimulator)

    ##### VISUALISATION
    layoutWF = "./Layout/BeltWasteRecyclingV1.txt"
    insiderSimulator.run_visualization(workflow,layoutWF)


    ####SIMULAZIONE
    # Run the simulation.
    reporter=InsiderReporter(insiderSimulator,workflow)
    #reporter=SimpleReporter()
    start_time = time.time()
    insiderSimulator.run_simulation(workflow,reporter)
    end_time = time.time()
    print(f"exec time: {end_time - start_time}")

    #### PRINT medie valori
    print("mean_cycle_time:", reporter.mean_cycle_time())
    print("mean_system_load:", reporter.mean_system_load())
    print("mean_task_sequence_time:", reporter.mean_requestUtilizationTimeTaskSeq())

    FiguresGenerator.generate_figures(insiderSimulator,"BeltWasteRecyclingV1_exponential")