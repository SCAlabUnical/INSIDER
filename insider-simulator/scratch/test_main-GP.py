from src.Insider.InsiderSimulator import *
from src.Insider.DeploymentGeneration import generateAllocation, evaluateAllocation
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

def objective(allocation,safeFile=False):

    ## Carico la frequenza di arrivo
    inputAverageArrivalTime = 1.0/InsiderUtil.getJsonKey( input_path+'constraints.json' , "rate")

    insider_simulator=InsiderSimulator(name_token="Req_",inputAverageArrivalTime=inputAverageArrivalTime,SIMULATION_DURATION=1*20*60,name="BeltWasteRecyclingVTest")
    insider_simulator.input_path = input_path
    insider_simulator.dictResources = InsiderUtil.getResourcesFromFile(input_path+'Resources.csv')
    insider_simulator.dictTasks = InsiderUtil.getTasksFromFile(input_path+'Tasks.csv')
    insider_simulator.jsonWorkflow = InsiderUtil.getJsonWorkflow(input_path+'Flow.json')
    insider_simulator.zfillLen = zfillLen

    timeout = 10
    if safeFile:
        timeout = 3600

    with stopit.ThreadingTimeout(timeout) as context_manager:
        try:
            generateAllocation(insider_simulator,allocation,boundResource,safeFile)

            insider_simulator.requestUtilizationTimeTaskSeq = dict()
            insider_simulator.resourceUtilizationTime = dict()
            insider_simulator.rhoCount = dict()
            parser=InsiderParser(insider_simulator)
            workflow=parser.parse()
            insider_simulator.run(workflow)
            if safeFile:
                FiguresGenerator.generate_figures(insider_simulator, image_path)
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

    ## pulisco il file di tutti i risultati delle simulazioni
    InsiderUtil.resetJsonSimResults(input_path+'sim_results.json')

    # perform the differential evolution search
    result = differential_evolution( objective, bounds, integrality=(True)*len(bounds), maxiter=100, popsize=4, workers=4, updating='deferred' )

    # salvo il risultato migliore e le figure dei grafici
    objective(result["x"],safeFile=True)

    print('Status : %s' % result['message'])
    print('Total Evaluations: %d' % result['nfev'])
    print("Best allocation: ",result["x"])
    print("Best cost: ",result["fun"])










