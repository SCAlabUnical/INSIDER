#differential evolution global optimization for the ackley multimodal objective function
import random

from scipy.optimize import differential_evolution

# objective function
def objective(v):
    # da sostituire con simulazione
    print(v)
    #x1, x2, x3, x4 , x5 = v
    return random.random() #(x1-3)**2 + (x2-8)**2 + (x3-4)**2 + (x4-3)**2 + (x5-5)**2

if __name__ == '__main__':
    # define range for input
    lenTasks = 18 # numero di task da allocare
    lenResources = 30 #10 # numero di risorse disponibili

    # define the bounds on the search
    bounds = [[1, lenResources]]*lenTasks
    print("bounds =", bounds )

    # perform the differential evolution search
    result = differential_evolution( objective, bounds, integrality=(True,)*lenTasks, maxiter=100, popsize=4, workers=1,updating='deferred')

    # summarize the result
    print('Status : %s' % result['message'])
    print('Total Evaluations: %d' % result['nfev'])
    # evaluate solution
    solution = result['x']
    evaluation = objective(solution)
    print('Solution: f(%s) = %.5f' % (solution, evaluation))

    for i in range(len(solution)):
        print('Task '+str(i+1) + ' on Resource '+str(solution[i]))
