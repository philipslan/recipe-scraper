import json
import re
import os
path = os.path.dirname(__file__)

TOOLS = []
APPLIANCES = ["oven","microwave","microwave oven","stove","toaster","oven broiler","broiler"]

# removing duplicates and preserving order  http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def load_tools():
    global TOOLS
    if len(TOOLS):
        return
    with open(os.path.join(path, 'tools.json')) as f:
    	TOOLS = json.load(f)

def find_tools(steps):
    tools_by_step = []
    all_tools = []
    
    # TODO mappings like basting-> requires baster, mix->requires spoon/fork/mixer, "turning + oven" => tongs
    # slice => knife
    # or if sliced or chopped are in ingredients

    # TODO go through all steps and if any step tool is believed to be from a previous step, remove it
    # from all_tools
    for (i,s) in enumerate(steps):
        step_tools = tools_for_step(s)
        tools_by_step.append(step_tools)
        
        # if it's preceded by "the" it's probably referring to a tool introduced earlier
        # TODO are all newly introduced tools preceded directly by "a"? might add this
        for st in step_tools:            
            if st in APPLIANCES or not re.findall(r"the\s*\w*\s*" + st, s):
                all_tools.append(st)
    
    all_tools = f7(all_tools)
    
    # TODO synthesize all step tools? i.e. if "pan" is in step 4 and
    #  "skillet" was in step 1, remove "skillet" as from tools
    #  as they're likely referring to the same thing
    
    return all_tools
    
    
def tools_for_step(step):
    load_tools()
    step = step.lower()
    
    recipe_tools = [t for t in TOOLS if t in step]
    
    # eliminate double-counting. prevent ["skillet", "large skillet"]
    # another method would be to sort by tool length descending and 
    # remove the matching tools from the sstep text as we go
    tools = []
    for rt1 in recipe_tools:
        unique = True
        for rt2 in recipe_tools:
            a1 = rt1 in APPLIANCES
            a2 = rt2 in APPLIANCES
            
            if a1 == a2 and rt1 in rt2 and rt1 != rt2 and len(rt1.split()) < len(rt2.split()):
                unique = False
        if unique:
            tools.append(rt1)
    
    # TODO should "tools for each step" include ones that are just continued
    #  use from previous steps? if not, add the "the" checker here
    return tools
        
    