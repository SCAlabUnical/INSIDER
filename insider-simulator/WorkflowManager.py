class WorkflowManager():

    def insider_add_var(wf, param):
        # param = {"name":"PLACE_NAME","type":"COMPUTE/NETWORK/STORAGE","resource":"RESOURCE_NAME"}
        # name and type is mandatory

        if "name" in param and "type" in param:
            auxVar = wf.add_var(param["name"])
            auxVar.insider_tag={"type":param["type"]}
            auxVar.successors = []
        else:
            raise Exception("name and type is mandatory")

        if "resource" in param:
            auxVar.put(param["resource"])

        if "labelName" in param:
            auxVar.insider_tag["labelName"] = param["labelName"]

        return auxVar


    def insider_add_event(wf,inflow,outflow,behavior, param, guard = None):
        # param = {"name":"PLACE_NAME","type":"COMPUTE/NETWORK/STORAGE","flow":"join/split/choice"}
        # name and type is mandatory

        if "name" in param and "type" in param:
            auxEvent = wf.add_event(inflow, outflow, behavior, name=param["name"], guard=guard)
            auxEvent.insider_tag={"type":param["type"]}
        else:
            raise Exception("name and type is mandatory")

        if "flow" in param:
            auxEvent.insider_tag["flow"] = param["flow"]

        if "labelName" in param:
            auxEvent.insider_tag["labelName"] = param["labelName"]

        return auxEvent