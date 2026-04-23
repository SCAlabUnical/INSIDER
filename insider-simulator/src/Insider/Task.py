class Task:

    ####### init #######
    id = -1
    type = -1 # 0 = Tc ; 1 = Tn ; 2 = Ts
    name = ""

    ####### Tc #######
    requestMilionsOfInstructions = -1 # milioni di istruzioni per completare il task
    """
    cpuFrequency = -1
    cpuCores = -1
    requiredFrequency = -1
    requiredRam = -1
    meanTc = []
    probalityTc = []
    serverTc = -1
    """

    ####### Tn #######
    requestTransferMB = -1 # mega byte da trasferire ( byte non bit ricordarsi di moltiplicare per 8)
    """
    bandwidth = -1
    uploadSpeed = -1
    downloadSpeed = -1
    meanTn = -1
    serverTn = -1
    """

    ####### Ts #######
    requestStoreMB = -1
    """
    queryDataRead = -1
    queryDataWrite = -1
    meanTs = -1
    serverTs = -1
    """

    ####### Allocation #######
    executor = None # riferimento alla risorsa su cui è stato schedulato

    ####### init #######
    def __init__(self, id, type):
            self.id = id
            self.type = type


    def __str__(self):
        return ""+str(self.id)

    def __repr__(self):
        return self.__str__()