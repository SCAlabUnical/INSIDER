class Node:

    ####### init #######
    id = -1
    type = -1 # 0 = Edge ; 1 = Cloud

    ####### Nc #######
    MIPS = -1
    cpuFrequency = -1
    cpuCores = -1
    ram = -1
    freeFrequency = -1
    freeRam = -1

    ####### Tn #######
    bandwidth = -1
    uploadSpeed = -1
    downloadSpeed = -1

    ####### Ts #######
    querySpeedRead = -1
    querySpeedWrite = -1

    ####### init #######
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __str__(self):
        return ""+str(self.id)

    def __repr__(self):
        return self.__str__()
