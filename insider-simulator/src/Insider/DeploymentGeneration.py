import shutil

#from src.Insider.InsiderSimulator import FiguresGenerator
from src.Insider.InsiderUtil import InsiderUtil

def generateAllocation(insider_simulator, listAllocation, boundResource):

    #listResourcesKey = list(insider_simulator.dictResources.keys())
    lisTasksKey = list(insider_simulator.dictTasks.keys())

    # cancello la vecchia allocazione
    insider_simulator.dictAllocation = dict()

    insider_simulator.allocationHash = InsiderUtil.allocationToHash(listAllocation, insider_simulator.zfillLen )

    workflowCost = 0

    for i in range(len(listAllocation)):
        #print("i =", i)
        #print("listAllocation =", int(listAllocation[i]-1))
        #print("K1",boundResource[i])
        #print("K2",int(listAllocation[i]))
        #print("K3",boundResource[i][int(listAllocation[i])] )

        #print("------------------")
        #print(i)
        #print(boundResource[i])
        #print(int(listAllocation[i]))
        #print(boundResource[i][int(listAllocation[i])])


        resName = boundResource[i][int(listAllocation[i])]  # listResourcesKey[int(listAllocation[i]-1)]
        #print("resName =", resName)
        if resName in insider_simulator.dictAllocation:
            insider_simulator.dictAllocation[resName].append(lisTasksKey[i])
        else:
            insider_simulator.dictAllocation[resName]= [lisTasksKey[i]]
            # pago solo una volta il costo di una risorsa anche se ha più task
            workflowCost = workflowCost + insider_simulator.dictResources[resName].cost

    #print("allocation:",insider_simulator.dictAllocation)

    # salvo il costo totale di questo workflow
    insider_simulator.workflowCost = workflowCost

    return


def evaluateAllocation(insider_simulator):
    #### Carico i vincoli

    constraints_mean_cycle_time = InsiderUtil.getJsonKey(insider_simulator.input_path+'constraints.json','mean_cycle_time')
    sim_result_cost = insider_simulator.workflowCost

    #jsonSimResult = InsiderUtil.getJsonDict(insider_simulator.input_path+'sim_result.json')
    sim_result_mean_cycle_time = insider_simulator.simResult['mean_cycle_time']
    sim_result_mean_work_time = insider_simulator.simResult['mean_work_time']

    jsonToAppend = dict()
    jsonToAppend["id"] = insider_simulator.allocationHash
    jsonToAppend["mean_cycle_time"] = round(sim_result_mean_cycle_time,6)
    jsonToAppend["mean_work_time"] = round(sim_result_mean_work_time,6)
    jsonToAppend["cost"] = round(sim_result_cost,6)

    if ( sim_result_mean_cycle_time > 0 and
            sim_result_mean_work_time > 0 and
            sim_result_mean_cycle_time <= constraints_mean_cycle_time and
            sim_result_mean_work_time <= constraints_mean_cycle_time      ):

        jsonToAppend["status"] = "success"
        InsiderUtil.appendJsonSimResults(insider_simulator.input_path+'sim_results.json', jsonToAppend)
        InsiderUtil.updateJsonBestAllocation(insider_simulator.input_path+'BestAllocation.json',insider_simulator)
        # se i vincoli sono soddisfatti ritorno il costo della simulazione

        print("sim_result_cost:",round(sim_result_cost,6))
        print("sim_result_mean_cycle_time",round(sim_result_mean_cycle_time,6))
        return sim_result_mean_cycle_time
    else:
        jsonToAppend["status"] = "constrains violation"
        InsiderUtil.appendJsonSimResults(insider_simulator.input_path+'sim_results.json', jsonToAppend)
        # se i vincoli non sono soddisfatti ritorno un valore molto alto per dire a GP che questa scelta è sbagliata
        return float('inf')
