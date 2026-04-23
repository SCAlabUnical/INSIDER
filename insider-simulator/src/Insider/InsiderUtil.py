import csv
import json

from Resource import Node
from Task import Task

import fasteners

from src.Insider.InsiderSimulator import FiguresGenerator

lock_sim_result = fasteners.InterProcessLock('../lock_sim_result')
lock_read_file = fasteners.InterProcessLock('../lock_read_file')
lock_best_allocation = fasteners.InterProcessLock('../lock_best_allocations')

class InsiderUtil:

    @staticmethod
    def getBound(dicTask,dictResource,inputPath):

        bound = []
        boundResource = []

        for i in range(len(dicTask.keys())):
            boundResource.append([])
        #print(boundResource)
        fixed = InsiderUtil.getJsonKey(inputPath+'constraints.json' , "fixed")
        #print("fixed:",fixed)
        #for key in fixed:
        #    print("key:",key)


        for i, keyTask in enumerate(dicTask):
            if keyTask in fixed:
                boundResource[i].append(fixed[keyTask])
            else:
                for keyResource in dictResource:
                    if dictResource[keyResource].type == dicTask[keyTask].type:
                        boundResource[i].append(keyResource)

        print("-----boundResource------ ")
        for row in boundResource:
            print(row)

        print("-----bound-------------- ")
        for row in boundResource:
            bound.append((0,len(row)-1))

        print(bound)

        return bound, boundResource


    @staticmethod
    def getTaskType(tt):
        if "Tc".lower() == tt.lower():
            return 0
        elif "Tn".lower() == tt.lower():
            return 1
        elif "Ts".lower() == tt.lower():
            return 2
        else:
            raise ValueError("Task type not recognized")

    @staticmethod
    def getResourcesFromFile(filename):
        with lock_read_file:
            dictResources = {}
            with open(filename, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if spamreader.line_num == 1:
                        continue

                    type = InsiderUtil.getTaskType(row[0][0]+row[0][1])
                    auxNode = Node(row[0], type)

                    ####### Nc #######
                    auxNode.cpuFrequency = float(row[4])
                    auxNode.cpuCores = float(row[3])
                    auxNode.freeFrequency = auxNode.cpuCores * auxNode.cpuFrequency
                    auxNode.MIPS = auxNode.cpuCores * auxNode.cpuFrequency * 1000
                    auxNode.ram = float(row[6])
                    auxNode.freeRam = float(row[6])
                    ####### Tn #######
                    auxNode.bandwidth = -1
                    auxNode.uploadSpeed =float( row[13])
                    auxNode.downloadSpeed = float(row[13])
                    ####### Ts #######
                    auxNode.querySpeedRead = float(row[15])
                    auxNode.querySpeedWrite = float(row[15])
                    auxNode.cost = float(row[17])

                    dictResources[auxNode.id]= auxNode

            # print resources
            #for key in dictResources:
            #    print("Resource:",dictResources[key].__dict__)

            return dictResources

    @staticmethod
    def getTasksFromFile(filename):
        with lock_read_file:
            dictTasks = {}
            with open(filename, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if spamreader.line_num == 1:
                        continue

                    from src.Insider.InsiderSimulator import InsiderParser
                    num = InsiderParser.getTaskType(row[0])

                    auxTask = Task(row[1], num)
                    auxTask.name = row[1]

                    if auxTask.type == 0:
                        auxTask.requestMilionsOfInstructions = float(row[2])
                    elif auxTask.type == 1:
                        auxTask.requestTransferMB = float(row[2])
                    elif auxTask.type == 2:
                        auxTask.requestStoreMB = float(row[2])
                    else:
                        raise ValueError("Task type not recognized")

                    dictTasks[auxTask.id] = auxTask

            #print tasks
            #for key in dictTasks:
            #    print("Task:",dictTasks[key].__dict__)

            return dictTasks

    @staticmethod
    def getJsonKey(filename, key):
        with lock_read_file:
            jFile = open(filename,'r')
            j = json.load(jFile)
            jFile.close()
            return j[key]

    @staticmethod
    def setJsonKeyValues(filename, dictKeyValues):
        with lock_read_file:
            jFile = open(filename,"w")
            jFile.write(json.dumps(dictKeyValues, indent=4))
            jFile.close()

    @staticmethod
    def getJsonWorkflow(filename):
        with lock_read_file:
            jFile = open(filename,'r')
            j = json.load(jFile)
            return j

    @staticmethod
    def allocationToHash(allocation,zfillLen):
        hash = ""
        for element in allocation:
            hash=hash+(str(int(element)).zfill(zfillLen))
        return hash

    @staticmethod
    def resetJsonSimResults(filename):
        j = dict()
        j["simulations"] = []
        jFile = open(filename,"w")
        jFile.write(json.dumps(j, indent=4))
        jFile.close()

    @staticmethod
    def resetJsonBestAllocation(filename):
        j = dict()
        j["id"] = str("")
        j["cost"] = -1
        j["mean_cycle_time"] = -1
        j["allocation"] = {}
        jFile = open(filename,"w")
        jFile.write(json.dumps(j, indent=4))
        jFile.close()


    @staticmethod
    def existsJsonSimResults(filename, idAllocation ):

        with lock_sim_result:

            jFile = open(filename,'r')
            j = json.load(jFile)
            jFile.close()

            for sim in j["simulations"] :
                if sim["id"] == idAllocation:  # and sim["status"] == "success":
                    print("id", idAllocation, " exists!!!")
                    # se esisiste questa simulazione eseguita con successo, ritorno il mean_cycle_time
                    if sim["mean_cycle_time"] == -1:
                        return float('inf')
                    else:
                        return sim["mean_cycle_time"]

            # altrimenti torno -2 , per indicare che non esiste
            return -1

    @staticmethod
    def appendJsonSimResults(filename, simResult ):

        with lock_sim_result:

            jFile = open(filename,'r')
            j = json.load(jFile)
            jFile.close()

            # aggiungo il risultato solo se non esiste l'ID della soluzione
            for sim in j["simulations"]:
                if sim["id"] == simResult["id"] and sim["status"] == "success":
                    print("id", simResult["id"], " exists!!!")
                    return

            j["simulations"].append(simResult)
            jFile = open(filename,"w")
            jFile.write(json.dumps(j, indent=4))
            jFile.close()

    @staticmethod
    def updateJsonBestAllocation(filename, insider_simulator ):

        newCost = insider_simulator.workflowCost
        mean_cycle_time = insider_simulator.simResult['mean_cycle_time']

        with lock_best_allocation:

            jFile = open(filename,'r')
            j = json.load(jFile)
            jFile.close()

            if j["id"] == "" or \
                    mean_cycle_time < j["mean_cycle_time"] or \
                    ( mean_cycle_time == j["mean_cycle_time"] and newCost < j["cost"] ) :

                j["id"] = ""+insider_simulator.allocationHash
                j["cost"] = round(newCost,6)
                j["mean_cycle_time"] = round(mean_cycle_time,6)
                j["allocation"] = insider_simulator.dictAllocation

                jFile = open(filename,"w")
                jFile.write(json.dumps(j, indent=4))
                jFile.close()

                FiguresGenerator.generate_figures(insider_simulator, insider_simulator.input_path+'images/')

