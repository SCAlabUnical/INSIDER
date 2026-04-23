import matplotlib.pyplot as plt
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp
from WorkflowManager import WorkflowManager

# Instantiate a simulation problem.
workflow = SimProblem()

# https://nl.mathworks.com/discovery/transfer-learning.html

# Define queues and other 'places' in the process.
Tn1_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn1_p", "type": "NETWORK"})
Tn2_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn2_p", "type": "NETWORK"})
Tn3_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn3_p", "type": "NETWORK"})
Tn4_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn4_p", "type": "NETWORK"})
Tn5_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn5_p", "type": "NETWORK"})
Tn6_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_p", "type": "NETWORK"})
Tn7_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn7_p", "type": "NETWORK"})
Tn8_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_p", "type": "NETWORK"})
Tc1_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc1_p", "type": "COMPUTE"})
Tc2_p_r1 = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_p_r1", "type": "COMPUTE"})
Tc2_p_r2 = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_p_r2", "type": "COMPUTE"})
Tc3_p_r1 = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_p_r1", "type": "COMPUTE"})
Tc3_p_r2 = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_p_r2", "type": "COMPUTE"})
Tc4_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc4_p", "type": "COMPUTE"})
Ts1_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts1_p", "type": "STORAGE"})
Ts2_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts2_p", "type": "STORAGE"})
Ts3_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts3_p", "type": "STORAGE"})
Ts4_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts4_p", "type": "STORAGE"})

# Define a 'places' with resources.
Tn1_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn1_r", "type": "NETWORK", "resource": "n1_r"})
Tn2_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn2_r", "type": "NETWORK", "resource": "n2_r"})
Tn3_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn3_r", "type": "NETWORK", "resource": "n3_r"})
Tn4_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn4_r", "type": "NETWORK", "resource": "n4_r"})
Tn5_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn5_r", "type": "NETWORK", "resource": "n5_r"})
Tn6_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_r", "type": "NETWORK", "resource": "n6_r"})
Tn7_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn7_r", "type": "NETWORK", "resource": "n7_r"})
Tn8_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn8_r", "type": "NETWORK", "resource": "n8_r"})
Tc1_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc1_r", "type": "COMPUTE", "resource": "c1_r"})
Tc2_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_r", "type": "COMPUTE", "resource": "c2_r"})
Tc3_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_r", "type": "COMPUTE", "resource": "c3_r"})
Tc4_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc4_r", "type": "COMPUTE", "resource": "c4_r"})
Ts1_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts1_r", "type": "STORAGE", "resource": "s1_r"})
Ts2_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts2_r", "type": "STORAGE", "resource": "s2_r"})
Ts3_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts3_r", "type": "STORAGE", "resource": "s3_r"})
Ts4_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts4_r", "type": "STORAGE", "resource": "s4_r"})


# Define events.
# Tn Task network
curr_token=1
name_token = "Req_"
Ts1_p.put(name_token + str(curr_token))

def Ts1_t(c,r):
    global curr_token
    curr_token= curr_token+1
    return [SimToken(name_token+str(curr_token), delay=exp(3)*60), SimToken(c, delay=exp(3)*60),
            SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Ts1_p, Ts1_r],[Ts1_p,  Ts1_p, Tn1_p, Ts1_r], Ts1_t,
                                  {"name":"Get pretrained network","type":"STORAGE"})

def Tn1_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Tn1_p, Tn1_r], [Tc1_p, Tn1_r], Tn1_t,
                                  {"name":"Tn1_t","type":"NETWORK"})

def Tc1_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tc1_p, Tc1_r], [Tn2_p, Tc1_r], Tc1_t,
                                  {"name":"Modify network","type":"COMPUTE"})

def Tn2_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Tn2_p, Tn2_r],[Tc2_p_r1, Ts2_p, Tn2_r], Tn2_t,
                                  {"name":"Tn2_t","type":"NETWORK", "flow":"And"})

def Ts2_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Ts2_p, Ts2_r], [Tn6_p, Ts2_r], Ts2_t,
                                  {"name":"Get training data","type":"STORAGE"})

def Tn6_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn6_p, Tn6_r], [Tc2_p_r2, Tn6_r], Tn6_t,
                                  {"name":"Tn6_t","type":"NETWORK"})

def Tc2_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tc2_p_r1, Tc2_p_r2, Tc2_r], [Tn3_p , Tc2_r], Tc2_t,
                                  {"name":"Retain network","type":"COMPUTE", "flow":"And"})

def Tn3_t(c,r):
    return [SimToken(c, delay=exp(3)*60),SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Tn3_p, Tn3_r], [Tc3_p_r1,Ts3_p, Tn3_r], Tn3_t,
                                  {"name":"Tn3_t","type":"NETWORK", "flow":"And"})

def Ts3_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Ts3_p, Ts3_r], [Tn7_p, Ts3_r], Ts3_t,
                                  {"name":"Ts3_t","type":"STORAGE"})

def Tn7_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn7_p, Tn7_r], [Tc3_p_r2, Tn7_r], Tn7_t,
                                  {"name":"Tn7_t","type":"NETWORK"})

def Tc3_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tc3_p_r1, Tc3_p_r2, Tc3_r], [Tn4_p , Tc3_r], Tc3_t,
                                  {"name":"Predict on new data","type":"COMPUTE", "flow":"And"})

def Tn4_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn4_p, Tn4_r], [Tc4_p, Tn4_r], Tn4_t,
                                  {"name":"Tn4_t","type":"NETWORK"})

def Tc4_t(c,r):
    return [SimToken(c, delay=exp(3)*60), SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tc4_p, Tc4_r], [Tn5_p , Tn8_p, Tc4_r], Tc4_t,
                                  {"name":"Result evaluation","type":"COMPUTE", "flow":"Or"})

def Tn5_t(c,r):
    return [SimToken(c, delay=exp(3)*60),SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn5_p, Tn5_r], [ Ts4_p, Tn5_r], Tn5_t,
                                  {"name":"Reject result","type":"NETWORK"})

def Tn8_t(c,r):
    return [SimToken(c, delay=exp(3)*60),SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn8_p, Tn8_r], [ Ts4_p, Tn8_r], Tn8_t,
                                  {"name":"Update network","type":"NETWORK"})

def Ts4_t(r):
    return [SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Ts4_p, Ts4_r], [Ts4_r], Ts4_t,
                                  {"name":"Ts4_t","type":"STORAGE", "flow":"Or"})

##### VISUALISATION
from insidervisualization import Visualisation
layoutWF = "./Layout/TransferLearning.txt"
v = Visualisation(workflow, layoutWF)
v.show("TransferLearning")
v.save_layout(layoutWF)



