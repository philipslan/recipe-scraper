import json
import os
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
                print trans_list
                print transform_helper([value],trans_list)
            # else:
        # for TRANSFORMATIONS[to_or_from][category]
        # pprint(TRANSFORMATIONS)
        # print "\n"
        # pprint(recipe)
        # recipe['ingredients'] = transform_helper(recipe['ingredients'],trans_list)

        ### FOR VEGAN ###
        # "cheeses": ["Asiago", "Carmody", "Cheddar", "Colby", "Cotija",
        # "Edam", "Enchilado", "Fontina", "Gouda", "Havarti",
        # "Longhorn", "Port Salut", "St. George", "Syrian"
        # ]

    elif category is 'low-carb' or category == 'low-sodium':
        # IMPORTANT for HEALTHY.json
        # "lowcarb-stopwords": ["almond", "wheat", "vegetable"],
        # "pasta": ["penne", "linguine", "fettuccine", "spaghetti"]
        ###
        
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
    else:
        print "Category not found"
    
    # return transformed_recipe

def transform_helper(ingredients,transformations):
    final = []
    for ingredient in ingredients:
        ing_array = ingredient.split()
        for i,word in enumerate(ing_array):
            if word in transformations:
                ing_array[i] = " or ".join(transformations[word]) if len(transformations[word]) > 1 else transformations[word][0]
        final.append(" ".join(ing_array))
    return final
