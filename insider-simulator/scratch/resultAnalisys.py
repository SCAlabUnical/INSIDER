import json
import os
import jmespath
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import savefig


# https://github.com/ashwin2rai/pareto_front/blob/master/Pareto.ipynb
# Faster than is_pareto_efficient_simple, but less readable.
def is_pareto_efficient(costs, return_mask = True):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :param return_mask: True to return a mask
    :return: An array of indices of pareto-efficient points.
        If return_mask is True, this will be an (n_points, ) boolean array
        Otherwise it will be a (n_efficient_points, ) integer array of indices.
    """
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index<len(costs):
        nondominated_point_mask = np.any(costs<costs[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1
    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype = bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient

######################### MAIN ##############################################################################

#relativePath = '../data/BeltWasteRecyclingVTest/'
relativePath = '../data/Taxi/'

savefig = True

listFile = os.listdir(relativePath)
listFile.sort()

for filename in listFile:
    if filename.endswith('sim_results.json'):

        with open( relativePath+filename,  'r') as f:
            result= json.load(f)

        print('#simulations=', len(result["simulations"]))

        # https://jmespath.org/examples.html
        test=jmespath.search("simulations[?cost < `30.0` && status == `success`][id,cost,mean_cycle_time]",result)

        filtered=[]
        filtered_dict={"id":[],"cost":[],"mean_cycle_time":[]}

        pareto = []

        for x in test:
            if(x[1]>0):
                filtered.append(x)
                filtered_dict["id"].append(x[0])
                filtered_dict["cost"].append(x[1])
                filtered_dict["mean_cycle_time"].append(x[2])
                pareto.append([x[2],x[1]])
        """
        plt.scatter(filtered_dict["mean_cycle_time"],filtered_dict["cost"])
        plt.xscale('log',base=2)
        #plt.yscale('log',base=10
        #plt.xscale('log')
        plt.xlabel("Mean Cycle Time")
        plt.ylabel("Cost")
        if savefig:
            plt.savefig(relativePath+'images/xy_'+filename+'.jpg')
        else:
            plt.show()
        """
        plt.close()
        rng = np.array(pareto) #np.random.RandomState(1134).rand(300, 2)
        a = is_pareto_efficient(np.array(rng))

        #plt.rcParams.update({'font.size': 10})
        #plt.rcParams["figure.figsize"] = (5.0,3.5)
        #plt.figure(figsize=(4.5, 3.0))

        #plt.figure().set_size_inches(3.2,1.4)
        #plt.figure().set_figwidth(2.4)
        #plt.figure().set_figheight(4)
        #print(plt.figure().get_figwidth())
        #print(plt.figure().get_figheight())


        #plt.rcParams.update({'font.size':18})
        #plt.rc('axes', titlesize=16)
        plt.rc('figure', titlesize=16)
        plt.rc('axes', labelsize=16 )

        plt.rcParams['pdf.fonttype'] = 42
        plt.rcParams['ps.fonttype'] = 42

        plt.scatter(x=rng[:,0],y=rng[:,1],c='b',marker='.')
        plt.scatter(x=np.where(a,rng[:,0],np.nan),y=np.where(a,rng[:,1],np.nan),c='r',alpha=0.3,marker='o',s=100)
        plt.xlabel("Request execution time (sec)")
        plt.ylabel("Cost per hours ($)")#,fontsize=14)

        #plt.xscale('log',base=2)

        #plt.yticks([9,10,11,12])
        #plt.xlim([0, 32])
        #plt.ylim([9, 12])
        if savefig:
            plt.savefig(relativePath+'images/pareto_'+filename+'.jpg')
            plt.savefig(relativePath+'images/pareto_'+filename+'.pdf')
    else:
        None
        #plt.show()