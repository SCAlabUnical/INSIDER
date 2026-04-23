import shutil

from src.Insider.DeploymentGeneration import generateAllocation, evaluateAllocation
from src.Insider.InsiderSimulator import InsiderSimulator, InsiderParser
from src.Insider.InsiderUtil import InsiderUtil

from scipy.optimize import differential_evolution
import stopit

# Global variables
image_path="../data/BeltWasteRecyclingVTest/images/"
input_path="../data/BeltWasteRecyclingVTest/"

zfillLen = 2
bounds , boundResource = InsiderUtil.getBound(InsiderUtil.getTasksFromFile(input_path+'Tasks.csv'),
                                              InsiderUtil.getResourcesFromFile(input_path+'Resources.csv'),
                                              input_path)

def objective(allocation, visualize=False):

    idAllocation = InsiderUtil.allocationToHash(allocation,zfillLen)
    mean_cycle_time = InsiderUtil.existsJsonSimResults(input_path+'sim_results.json',idAllocation)
    if mean_cycle_time >= 0:
        return mean_cycle_time

    ## Carico la frequenza di arrivo
    inputAverageArrivalTime = 1.0/InsiderUtil.getJsonKey( input_path+'constraints.json' , "rate")

    insider_simulator=InsiderSimulator(name_token="Req_",inputAverageArrivalTime=inputAverageArrivalTime,SIMULATION_DURATION=6*60*60,name="BeltWasteRecyclingVTest")
    insider_simulator.input_path = input_path
    insider_simulator.dictResources = InsiderUtil.getResourcesFromFile(input_path+'Resources.csv')
    insider_simulator.dictTasks = InsiderUtil.getTasksFromFile(input_path+'Tasks.csv')
    insider_simulator.jsonWorkflow = InsiderUtil.getJsonWorkflow(input_path+'Flow.json')
    insider_simulator.zfillLen = zfillLen

    timeout = 60
    if visualize:
        timeout = 3600

    with stopit.ThreadingTimeout(timeout) as context_manager:
        try:
            generateAllocation(insider_simulator,allocation,boundResource)

            insider_simulator.requestUtilizationTimeTaskSeq = dict()
            insider_simulator.resourceUtilizationTime = dict()
            insider_simulator.rhoCount = dict()
            parser=InsiderParser(insider_simulator)
            workflow=parser.parse()
            insider_simulator.run(workflow)

            #insider_simulator.visualize_sim(workflow=workflow,input_path=input_path,image_path=image_path)

        except Exception as e:
            #print("eeee:",e.with_traceback())
            jsonToAppend = dict()
            jsonToAppend["id"] = insider_simulator.allocationHash
            jsonToAppend["mean_cycle_time"] = round(-1,6)
            jsonToAppend["mean_work_time"] = round(-1,6)
            jsonToAppend["cost"] = round(insider_simulator.workflowCost,6)
            jsonToAppend["status"] = type(e).__name__
            InsiderUtil.appendJsonSimResults(insider_simulator.input_path+'sim_results.json', jsonToAppend)
            print("stopit:", type(e).__name__)
            return float('inf')
            #return insider_simulator.workflowCost+100

    if context_manager.state == context_manager.EXECUTED:
        return evaluateAllocation(insider_simulator)
    elif context_manager.state == context_manager.TIMED_OUT:
        print("timed out")
        return float('inf')
        # return insider_simulator.workflowCost+100


if __name__ == '__main__':

    maxiterList = [10,100]

    for i, maxiter in enumerate( maxiterList):
        ## pulisco il file di tutti i risultati delle simulazioni
        InsiderUtil.resetJsonSimResults(input_path+'sim_results.json')
        InsiderUtil.resetJsonBestAllocation(input_path+'BestAllocation.json')

        # perform the differential evolution search
        result = differential_evolution( objective, bounds, integrality=(True)*len(bounds), maxiter=maxiter, popsize=16, workers=16, updating='deferred' )

        shutil.copy(input_path + 'sim_results.json',
                    input_path + str(maxiter) + "-" + str(i) + "-"+ 'sim_results.json')
        shutil.copy(input_path + 'BestAllocation.json',
                    input_path + str(maxiter) + "-" + str(i) + "-"+ 'BestAllocation.json')

        #objective(result["x"],True)

        print('Status : %s' % result['message'])
        print('Total Evaluations: %d' % result['nfev'])
        print("Best allocation: ",result["x"])
        print("Best cost: ",result["fun"])

    shutil.copy(input_path + 'console.out',
                input_path + str(maxiter) + "-" + 'console.out')










