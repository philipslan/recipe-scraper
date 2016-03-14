import json
import os
import re
from reverser import reverse
path = os.path.dirname(__file__)

from pprint import pprint

TRANSFORMATIONS = {'to':{},'from':{}}

def load_transformations(category):
    global TRANSFORMATIONS
    if category in TRANSFORMATIONS['to']:
        return
    with open(os.path.join(path, category + '.json')) as f:
    	TRANSFORMATIONS['to'][category] = json.load(f)
        TRANSFORMATIONS['from'][category] = {key: reverse(TRANSFORMATIONS['to'][category][key]) for key in TRANSFORMATIONS['to'][category]}

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
        for ing in ingredient.split():
            if ing in trans_list:
                return True
    return False
        
# to_category is 'to' or 'from'
def transform(recipe, category, to_or_from):
    trans_list = []
    if category is 'vegetarian' or category is vegan:
        trans_list = TRANSFORMATIONS[to_or_from][category]['trans']
        for key,value in recipe.iteritems():
            if key == "title":
                recipe[key] = transform_helper([value],trans_list)[0]
            else:
                recipe[key] = transform_helper(value,trans_list)
        pprint(recipe)

    elif category is 'low-carb' or category == 'low-sodium':
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
    else:
        print "Category not found"
    
    # return transformed_recipe

def transform_helper(ingredients,transformations):
    final = []
    for ingredient in ingredients:
        for key,val in transformations.iteritems():
            replace = " or ".join(val) if len(val) > 1 else val[0]
            ingredient = re.sub(key,replace,ingredient.lower())
        final.append(ingredient)
    return final
