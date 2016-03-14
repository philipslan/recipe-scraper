'''Version 0.1'''
import json
from ingredients import ingredients
from methods import methods
from tools import tools
from transformations import transformations
import scraper
from pprint import pprint

PREPTOOLS = {'fork':['mixed'],'knife':['chopped','sliced','minced','diced'], 'grater':['grated'], 'mortar and pestle':['crushed']}
METHODTOOLS = {'baster':['basting'], 'oven':['bake','broil'], 'fork':['mix']}

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
    
def recipe_by_steps(directions, ingredients, methods_by_step, tools_by_step): 
    steps = []
    for (i, d) in enumerate(directions):
        step = {}
        step_methods = methods_by_step[i]
        step_tools = tools_by_step[i]
        
        for sm in step_methods:
            for t in METHODTOOLS:
                if sm in METHODTOOLS[t] and t not in step_tools:
                    tools_by_step[i].append(t)
                    
                    
        step_ingredients = []
        for ingredient in ingredients:
            ingredient_words = ingredient['name'].split()
            for w in ingredient_words:
                if w in d:
                    step_ingredients.append(ingredient['name'])
                    break
        
        step['methods'] = methods_by_step[i]
        step['tools'] = tools_by_step[i]
        step['ingredients'] = step_ingredients
        
        steps.append(step)
    return steps
    

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    results = {}
    results['url'] = url

    recipe = scraper.get_recipe(url)
    if recipe == None:
        return None

    unit_measure, regex = ingredients.load_ingredient_data()
    results['ingredients'] = []
    for ing in recipe['ingredients']:
        results['ingredients'].append(ingredients.parse_ingredients(ing, unit_measure, regex))

    primary_cooking_methods, methods_by_step, cooking_methods = methods.find_all_methods(recipe['title'],recipe['directions'])
    results['primary cooking method'] = primary_cooking_methods
    results['cooking methods'] = cooking_methods

    tools_by_step, all_tools = tools.find_tools(recipe['directions'])
    results['cooking tools'] = all_tools

    for ingredient in results['ingredients']:
        for t in PREPTOOLS:
            if ingredient['preparation'] in PREPTOOLS[t]:
                results['cooking tools'].append(t)

    for method in results['cooking methods']:
        for t in METHODTOOLS:
            if method in METHODTOOLS[t]:
                results['cooking tools'].append(t)

    results['cooking tools'] = remove_duplicates(results['cooking tools'])
    
    if transformations.is_category('vegetarian', recipe['ingredients']):
        new_recipe = transformations.transform(recipe,'vegetarian','to')
    else:
        new_recipe = transformations.transform(recipe,'vegetarian','from')
    
    # pprint(results)
    pprint(new_recipe)
    return results
    
    

def parse_recipe(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. Also returns recipe divided
    into steps which each contain methods, tools and ingredients'''
    results = {}
    results['url'] = url

    recipe = scraper.get_recipe(url)
    if recipe == None:
        return None

    unit_measure, regex = ingredients.load_ingredient_data()
    results['ingredients'] = []
    for ing in recipe['ingredients']:
        results['ingredients'].append(ingredients.parse_ingredients(ing, unit_measure, regex))

    primary_cooking_methods, methods_by_step, cooking_methods = methods.find_all_methods(recipe['title'],recipe['directions'])
    results['primary cooking method'] = primary_cooking_methods
    results['cooking methods'] = cooking_methods

    tools_by_step, all_tools = tools.find_tools(recipe['directions'])
    results['cooking tools'] = all_tools


    for ingredient in results['ingredients']:
        for t in PREPTOOLS:
            if ingredient['preparation'] in PREPTOOLS[t]:
                results['cooking tools'].append(t)

    for method in results['cooking methods']:
        for t in METHODTOOLS:
            if method in METHODTOOLS[t]:
                results['cooking tools'].append(t)

    results['cooking tools'] = remove_duplicates(results['cooking tools'])
    steps = recipe_by_steps(recipe['directions'],results['ingredients'],methods_by_step,tools_by_step)
    
    return {'results':results, 'steps':steps, 'imageUrl':recipe['imageUrl']}

    
    
    
    

