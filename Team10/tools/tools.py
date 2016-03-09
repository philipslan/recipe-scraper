import json
import re
TOOLS = []

def load_tools():
    global TOOLS
    if len(TOOLS):
        return
    with open('tools/tools.json') as f:
    	TOOLS = json.load(f)

def find_tools(steps):
    tools_by_step = []
    all_tools = []

    for (i,s) in enumerate(steps):
        step_tools = tools_for_step(s)
        tools_by_step.append(step_tools)
        
        # if it's preceded by "the" it's probably referring to a tool introduced earlier
        for st in step_tools:            
            if not re.findall(r"the \w* " + st, s):
                all_tools.append(st)
    
    print tools_by_step
    print all_tools
    
    # TODO synthesize all step tools? i.e. if "pan" is in step 4 and
    #  "skillet" was in step 1, remove "skillet" as from tools
    #  as they're likely referring to the same thing
    
    
    
def tools_for_step(step):
    load_tools()
    step = step.lower()
    
    recipe_tools = [t for t in TOOLS if t in step]
    
    # eliminate double-counting. prevent ["skillet", "large skillet"]
    # another method would be to sort by tool length descending and 
    # remove the matching tools from the step text as we go
    tools = []
    for rt1 in recipe_tools:
        unique = True
        for rt2 in recipe_tools:
            if rt1 in rt2 and rt1 != rt2 and len(rt1.split()) < len(rt2.split()):
                unique = False
        if unique:
            tools.append(rt1)
    
    # TODO should "tools for each step" include ones that are just continued
    #  use from previous steps? if not, add the "the" checker here
    return tools
        
    