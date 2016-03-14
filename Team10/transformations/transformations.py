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

def is_category(category, ingredients, title):
    trans_list = {}
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

    if category.lower() in title.lower():
        return True
    regex = ""
    for i,x in enumerate(trans_list):
        if i == len(trans_list) - 1:
            regex += x
        else:
            regex += x + "|"
    for ingredient in ingredients:
        if len(re.findall(regex,ingredient)):
            return False
    return True

# to_category is 'to' or 'from'
def transform(recipe, category, to_or_from, typ=None):
    trans_list = {}
    if category == 'vegetarian' or category == 'vegan':
        trans_list = TRANSFORMATIONS[to_or_from][category]['trans']
        typ = 'veg'
    elif category == 'low-carb' or category == 'low-sodium':
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
        typ = 'healthy'
    for key,value in recipe.iteritems():
        if key == "imageUrl":
            pass
        elif key == "title":
            recipe[key] = transform_helper([value], trans_list, typ, to_or_from, key, category)[0]
        else:
            recipe[key] = transform_helper(value,trans_list, typ, to_or_from, key, category)
    return recipe

def transform_helper(ingredients, transformations, typ, to_or_from, other, category):
    final = []
    original_ingredients = ingredients[:]
    for i in xrange(len(ingredients)):
        for key,val in transformations.iteritems():
            replace = " or ".join(val) if len(val) > 1 else val[0]
            ingredients[i] = re.sub(key,replace,ingredients[i].lower())


        if original_ingredients[i] != ingredients[i]:
            if typ == 'veg':
                if to_or_from == 'to':
                    ingredients[i] = re.sub(r"ground",r"crumbled",ingredients[i].lower())
                else:
                    ingredients[i] = re.sub(r"crumbled",r"ground",ingredients[i].lower())

        final.append(ingredients[i])


    if typ is "veg":
        if other is "title" and to_or_from is "from" and re.findall(r"vegetarian|vegan", final[0].lower()):
            final[0] = re.sub(r"vegetarian |vegan ", "", final[0].lower())
        elif [i.lower() for i in original_ingredients] == [i.lower() for i in ingredients]: # nothing changed
            if other is "ingredients":
                final.append('crumbled bacon')
            if other is"directions":
                final.append('Add crumbled bacon on top.')

    # Change title to include what we transformed into
    if other is "title" and to_or_from is "to" and category not in final[0].lower():
        final[0] = category + " " + final[0]
        final[0] = final[0].title()


    return final


