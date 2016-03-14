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
    if category is 'vegetarian' or category is 'vegan':
        trans_list = TRANSFORMATIONS[to_or_from][category]['trans']
        typ = 'veg'
    elif category is 'low-carb' or category == 'low-sodium':
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
        typ = 'healthy'
    for key,value in recipe.iteritems():
        if key == "title":
            recipe[key] = transform_helper([value],trans_list, typ, to_or_from, key)[0]
        else:
            recipe[key] = transform_helper(value,trans_list, typ, to_or_from, key)
    return recipe

def transform_helper(ingredients, transformations, typ,to_or_from, other):
    ingredients = [i.lower() for i in ingredients]
    final = []
    original_ingredients = ingredients[:]
    for i in xrange(len(ingredients)):
        for key,val in transformations.iteritems():
            replace = " or ".join(val) if len(val) > 1 else val[0]
            ingredients[i] = re.sub(key,replace,ingredients[i])
        if original_ingredients[i] != ingredients[i]:
            if typ == 'veg':
                if to_or_from == 'to':
                    ingredients[i] = re.sub("ground","crumbled",ingredients[i])
                else:
                    ingredients[i] = re.sub("crumbled","ground",ingredients[i])
            # if typ == 'healthy':

        final.append(ingredients[i])

    if other == "title" and typ == "veg" and re.findall(r"vegetarian|vegan", final[0].lower()):
        final[0] = re.sub(r"vegetarian |vegan ", "", final[0].lower())
    elif original_ingredients == ingredients and typ == 'veg': # nothing changed
        if other == "ingredients":
            final.append('crumbled bacon')
        if other == "directions":
            final.append('Add crumbled bacon on top.')

    return final


