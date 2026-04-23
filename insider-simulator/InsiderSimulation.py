import numpy as np

class InsiderSimulator:
    def __init__(self, inputAverageArrivalTime, SIMULATION_DURATION):
        self.inputAverageArrivalTime = inputAverageArrivalTime
        self.SIMULATION_DURATION = SIMULATION_DURATION
        self.name_token = "Req_"
        self.rhoCount = dict()
        self.resourceUtilizationTime = dict()
        self.requestUtilizationTimeTaskSeq = dict()

    @staticmethod
    def getTasktype(tt):
        if "Tc".lower() == tt.lower():
            return 0
        elif "Tn".lower() == tt.lower():
            return 1
        elif "Ts".lower() == tt.lower():
            return 2
        else:
            raise ValueError("Task type not recognized")


    def getServiceTime(self,nameTask, dictTasks):
        duration = np.random.exponential(self.getAvgServiceTime(nameTask, dictTasks))


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


    def updateReourceUtilizationTime(self,nameToken, duration):
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

    def updaterRhoCount(self, nameTask, duration):
        if nameTask in self.rhoCount:
            self.rhoCount[nameTask] = self.rhoCount[nameTask] + duration
        else:
            self.rhoCount[nameTask] = duration


    def run_visualization(self,workflow,layoutWF):

        from insidervisualization import Visualisation
        #layoutWF = "./Layout/BeltWasteRecyclingV1.txt"
        v = Visualisation(workflow, layoutWF)
        v.show(layoutWF)
        v.save_layout(layoutWF)

    def run_simulation(self,workflow,reporter):
        workflow.simulate(self.SIMULATION_DURATION, reporter)