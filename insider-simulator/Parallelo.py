import matplotlib.pyplot as plt
import simpn.visualisation as vis
from simpn.simulator import SimProblem, SimVar
from simpn.simulator import SimToken
from random import expovariate as exp
from random import uniform
from simpn.reporters import Reporter
from WorkflowManager import WorkflowManager

# Instantiate a simulation problem.
workflow = SimProblem()


# Define queues and other 'places' in the process.
Tn1_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn1_p", "type": "NETWORK"})
Tn2_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn2_p", "type": "NETWORK"})
Tn3_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn3_p", "type": "NETWORK"})
Tn4_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn4_p", "type": "NETWORK"})
Tn5_p = WorkflowManager.insider_add_var(workflow, {"name": "Tn5_p", "type": "NETWORK"})
Tn6_p1 = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_p1", "type": "NETWORK"})
Tn6_p2 = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_p2", "type": "NETWORK"})
Tc1_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc1_p", "type": "COMPUTE"})
Tc2_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_p", "type": "COMPUTE"})
Tc3_p = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_p", "type": "COMPUTE"})
Ts1_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts1_p", "type": "STORAGE"})
Ts2_p = WorkflowManager.insider_add_var(workflow, {"name": "Ts2_p", "type": "STORAGE"})

# Define a 'places' with resources.
Tn1_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn1_r", "type": "NETWORK", "resource": "n1_r"})
Tn2_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn2_r", "type": "NETWORK", "resource": "n2_r"})
Tn3_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn3_r", "type": "NETWORK", "resource": "n3_r"})
Tn4_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn4_r", "type": "NETWORK", "resource": "n4_r"})
Tn5_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn5_r", "type": "NETWORK", "resource": "n5_r"})
Tn6_r = WorkflowManager.insider_add_var(workflow, {"name": "Tn6_r", "type": "NETWORK", "resource": "n6_r"})
Tc1_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc1_r", "type": "COMPUTE", "resource": "c1_r"})
Tc2_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc2_r", "type": "COMPUTE", "resource": "c2_r"})
Tc3_r = WorkflowManager.insider_add_var(workflow, {"name": "Tc3_r", "type": "COMPUTE", "resource": "c3_r"})
Ts1_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts1_r", "type": "STORAGE", "resource": "s1_r"})
Ts2_r = WorkflowManager.insider_add_var(workflow, {"name": "Ts2_r", "type": "STORAGE", "resource": "s2_r"})


# Define events.
# Tn Task network
curr_token=1
name_token = "Req_"
Tn1_p.put(name_token + str(curr_token))

def Tn1_t(c,r):
  global curr_token
  curr_token= curr_token+1
  return [SimToken(name_token+str(curr_token), delay=exp(3)*60), SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn1_p, Tn1_r],[Tn1_p,  Tc1_p, Tn1_r], Tn1_t,
                                  {"name":"Tn1_t","type":"NETWORK"})

def Tc1_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Tc1_p, Tc1_r], [Tn2_p, Tn3_p, Tc1_r], Tc1_t,
                                  {"name":"Tc1_t","type":"COMPUTE","flow":"And"})

def Tn2_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Tn2_p, Tn2_r],[Ts1_p, Tn2_r], Tn2_t,
                                  {"name":"Tn2_t","type":"NETWORK"})

def Tn3_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Tn3_p, Tn3_r], [Ts2_p, Tn3_r], Tn3_t,
                                  {"name":"Tn3_t","type":"NETWORK"})

def Ts1_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow, [Ts1_p, Ts1_r], [Tn4_p, Ts1_r], Ts1_t,
                                  {"name":"Ts1_t","type":"STORAGE"})

def Ts2_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Ts2_p, Ts2_r], [Tn5_p, Ts2_r], Ts2_t,
                                  {"name":"Ts2_t","type":"STORAGE"})

def Tn4_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn4_p, Tn4_r], [Tc2_p, Tn4_r], Tn4_t,
                                  {"name":"Tn4_t","type":"NETWORK"})

def Tn5_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tn5_p, Tn5_r], [Tc3_p, Tn5_r], Tn5_t,
                                  {"name":"Tn5_t","type":"NETWORK"})

def Tc2_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tc2_p, Tc2_r], [Tn6_p1, Tc2_r], Tc2_t,
                                  {"name":"Tc2_t","type":"COMPUTE"})

def Tc3_t(c,r):
  return [SimToken(c, delay=exp(3)*60), SimToken(r)]
WorkflowManager.insider_add_event(workflow,[Tc3_p, Tc3_r], [Tn6_p2, Tc3_r], Tc3_t,
                                  {"name":"Tc3_t","type":"COMPUTE"})

def Tn6_t(c1, c2,r):
  return [SimToken(r)]
r = WorkflowManager.insider_add_event(workflow,[Tn6_p1, Tn6_p2, Tn6_r], [Tn6_r], Tn6_t,
                                  {"name":"Tn6_t","type":"NETWORK","flow":"And"}, guard=lambda c1, c2, r: c1 == c2 )


## Reporter statistics
#
class InsiderReporter(Reporter):

  def __init__(self):

    self.arrival_times = dict()
    self.start_times = dict()
    self.complete_times = dict()
    self.total_wait_time = 0
    self.total_proc_time = 0
    self.wait_time= dict()
    self.time_num_token = [0] * SIMULATION_DURATION

  def callback(self, timed_binding):
    (binding, time, event) = timed_binding
    #print("###")
    #print(timed_binding)
    #print(binding)
    #print(paralleloConRisorsa)
    #print("---")
    #print(timed_binding)
    #print(binding[0][0])
    #print(binding[0][1])
    #print(binding[0][1].time)
    #print(time)
    #print(event)

    if event.get_id() == "Tn1_t":
      c_id = binding[0][1].value
      #print(c_id)
      self.arrival_times[c_id] = time
      for i in range(int(time),SIMULATION_DURATION):
           self.time_num_token[i]+=1
    elif event.get_id() == "Tn6_t":
      c_id = binding[0][1].value
      #print(c_id)
      self.complete_times[c_id] = time
      for i in range(int(time),SIMULATION_DURATION):
           self.time_num_token[i]-=1
      #print("COMPLETED "+c_id)
    if event.get_id() != "Tn1_t":
      for bind in binding:
        waiting=self.wait_time.get(bind[1].value,0)
        waiting=waiting+time-bind[1].time
        self.wait_time[bind[1].value]=waiting
        #print("waiting:", waiting)

  def mean_cycle_time(self):
    num_completed=len(self.complete_times.keys())
    #print(num_completed)
    mean_cycle_time=0
    for c_id in self.complete_times.keys():
      mean_cycle_time=mean_cycle_time+(self.complete_times[c_id]-self.arrival_times[c_id])/num_completed
    return mean_cycle_time

  def mean_system_load(self):
      mean_throughput=0
      for elem in self.time_num_token:
          mean_throughput+=elem
      return mean_throughput / len(self.time_num_token)

##### VISUALISATION
from insidervisualization import Visualisation
layoutWF = "./Layout/Parallelo.txt"
v = Visualisation(workflow, layoutWF)
v.show("Parallelo")
v.save_layout(layoutWF)


####SIMULAZIONE
# Run the simulation.
#myPetri.simulate(120, SimpleReporter())
SIMULATION_DURATION = 20*60
reporter=InsiderReporter()
workflow.simulate(SIMULATION_DURATION, reporter)


#print(reporter.wait_time)

x_wait_time= []
y_wait_time= []
x_complete_times= []
y_complete_times= []
x_time_nume_token= []
y_time_nume_token= []
for key in reporter.wait_time.keys():
  if key.startswith(name_token):
    #print(f"{key}: {reporter.wait_time[key]}")
    x_wait_time.append(key)
    y_wait_time.append(reporter.wait_time[key])
    try:
      y_complete_times.append(reporter.complete_times[key]-reporter.arrival_times[key])
      x_complete_times.append(key)
    except:
      print("except:",key)

### FINE SIMULAZIONE

plt.figure(figsize=(15,10))
plt.plot(x_wait_time, y_wait_time, color="blue")
plt.xlabel("Request")
plt.xticks(rotation=45)
plt.ylabel("wait_time")
plt.savefig("./images/Parallelo_wait_time.png")
plt.close()

plt.figure(figsize=(15,10))
plt.plot(x_complete_times, y_complete_times, color="blue")
plt.xlabel("Request")
plt.xticks(rotation=45)
plt.ylabel("cycle_time")
plt.savefig("./images/Parallelo_cycle_time.png")
plt.close()

x_time_nume_token= range(0, SIMULATION_DURATION)
y_time_nume_token= reporter.time_num_token

plt.figure(figsize=(15,10))
plt.plot(x_time_nume_token, y_time_nume_token, color="blue")
plt.xlabel("Time")
plt.xticks(rotation=45)
plt.ylabel("System load")
plt.savefig("./images/Parallelo_system_load.png")
plt.close()

print("mean_cycle_time:",reporter.mean_cycle_time())
print("mean_system_load:", reporter.mean_system_load())
print("mean_throughput:", len(x_complete_times)/SIMULATION_DURATION )