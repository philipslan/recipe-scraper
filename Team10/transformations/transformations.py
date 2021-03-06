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
    if category == 'vegetarian' or category == 'vegan':
        load_transformations(category)
        trans_list = TRANSFORMATIONS['to'][category]['trans']
    elif category == 'low-carb' or category == 'low-sodium':
        load_transformations('healthy')
        trans_list = TRANSFORMATIONS['to']['healthy'][category]
    elif category == 'chinese' or category == 'italian':
        load_transformations('cuisine')
        trans_list = TRANSFORMATIONS['to']['cuisine'][category]
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


def transform(recipe, category, to_or_from, typ=None):
    trans_list = {}
    if category == 'vegetarian' or category == 'vegan':
        trans_list = TRANSFORMATIONS[to_or_from][category]['trans']
        typ = 'veg'
    elif category == 'low-carb' or category == 'low-sodium':
        trans_list = TRANSFORMATIONS[to_or_from]['healthy'][category]
        typ = 'healthy'
    elif category == 'chinese' or category == 'italian':
        trans_list = TRANSFORMATIONS[to_or_from]['cuisine'][category]
        typ = 'cuisine'
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

    # detect cheese + descriptor
    if category == "chinese" or category == "vegan":
        cheeses = [r"swiss", r"feta", r"blue", r"american", r"provolone", r"mozzarella",
        r"parmesan", r"asiago", r"carmody", r"cheddar", r"colby", r"cotija", r"edam",
        r"enchilado", r"fontina", r"gouda", r"havarti", r"longhorn"]

    for i in xrange(len(ingredients)):
        if re.findall(r'cheese', ingredients[i], re.I):
            if category == "chinese" and to_or_from == "to":
                ingredients[i] = re.sub(r' cheese', r'', ingredients[i].lower())
                for cheese in cheeses:
                    regex = " and " + cheese + "|, " + cheese + "|" + cheese + " |" + cheese + ", |"+ cheese
                    ingredients[i] = re.sub(regex, r'', ingredients[i].lower())
            elif category == "vegan" and to_or_from == "to":
                ingredients[i] = re.sub(r'cheese', r'soy cheese', ingredients[i].lower())
                for cheese in cheeses:
                    regex = " and " + cheese + "|, " + cheese + "|" + cheese + " |" + cheese + ", "
                    ingredients[i] = re.sub(regex, r'', ingredients[i].lower())

        for key, val in transformations.iteritems():
            if key == "" or key == " ":
                pass
            else:
                replace = " or ".join(val) if len(val) > 1 else val[0]
                ingredients[i] = re.sub(key,replace,ingredients[i].lower())
        # Getting rid of commas and double spaces in ingredients
        if other == "ingredients":
            ingredients[i] = re.sub("  |, "," ",ingredients[i])
            original_ingredients[i] = ingredients[i]
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
        elif [i.lower() for i in original_ingredients] == [i.lower() for i in ingredients] and to_or_from == "from":
            if other is "ingredients":
                final.append('1 teaspoon crumbled bacon')
            if other is"directions":
                final.append('Add crumbled bacon on top.')

    # Change title to include what we transformed into
    if other is "title" and to_or_from is "to" and category not in final[0].lower():
        if typ == 'cuisine':
            final[0] = category + " Style " + final[0]
            final[0] = final[0].title()
        else:
            final[0] = category + " " + final[0]
            final[0] = final[0].title()

    return final


