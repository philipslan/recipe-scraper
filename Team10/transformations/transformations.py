import json
import os
from reverser import reverse
path = os.path.dirname(__file__)
TRANSFORMATIONS = {}

def load_transformations(category):
    global TRANSFORMATIONS
    if category in TRANSFORMATIONS['to']:
        return
    with open(os.path.join(path, category + '.json')) as f:
    	TRANSFORMATIONS['to'][category] = json.load(f)
        TRANSFORMATIONS['from'][category] = reverse(TRANSFORMATIONS['to'][category])

def is_category(category, ingredients):
    
    trans_list = []
    
    if category == 'vegetarian':
        load_transformations(category)
        trans_list = TRANSFORMATIONS['to'][category]['trans']
    elif category == 'vegan':
        load_transformations(category)
        trans_list = TRANSFORMATIONS['to'][category]['trans']
    elif category == 'low-carb':
        load_transformations('healthy')
        trans_list = TRANSFORMATIONS['to']['healthy'][category]
    elif category == 'low-sodium':
        load_transformations('healthy')
        trans_list = TRANSFORMATIONS['to']['healthy'][category]
    else:
        print "Category not found"
            
    for ingredient in ingredients:
        if ingredient in trans_list:
            return False
    return True
        
        
# to_category is 'to' or 'from'
def transform(recipe, category, to_or_from):
    transformed_recipe = {}
    
    trans_list = []
    if category == 'vegetarian':
        trans_list = TRANSFORMATIONS[to_or_from][category]['trans']
    elif category == 'vegan':
        trans_list = TRANSFORMATIONS[to_or_from][category]['trans']
    elif category == 'low-carb':
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
    elif category == 'low-sodium':
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
    else:
        print "Category not found"
    
    
    return transformed_recipe
    
    
    
    
