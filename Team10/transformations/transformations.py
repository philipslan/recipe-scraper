import json
import os
path = os.path.dirname(__file__)
TRANSFORMATIONS = {}

def load_transformations(category):
    global TRANSFORMATIONS
    if category in TRANSFORMATIONS:
        return
    with open(os.path.join(path, category + '.json')) as f:
    	TRANSFORMATIONS[category] = json.load(f)

def is_vegetarian(ingredients):
    load_transformations('vegetarian')
    veggie_trans = TRANSFORMATIONS['vegetarian']['trans']
    
    for ingredient in ingredients:
        if ingredient in veggie_trans:
            return False
    return True
        