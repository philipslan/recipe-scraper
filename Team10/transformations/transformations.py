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

def is_category(category, ingredients):
    
    trans_list = []
    
    if category == 'vegetarian':
        load_transformations('vegetarian')
        trans_list = TRANSFORMATIONS[category]['trans']
    elif category == 'vegan':
        load_transformations('vegan')
        trans_list = TRANSFORMATIONS[category]['trans']
    elif category == 'low-carb':
        load_transformations('healthy')
        trans_list = TRANSFORMATIONS['healthy'][category]
    elif category == 'low-sodium':
        load_transformations('healthy')
        trans_list = TRANSFORMATIONS['healthy'][category]
    else:
        print "Category not found"
            
    for ingredient in ingredients:
        if ingredient in trans_list:
            return False
    return True
        
        
