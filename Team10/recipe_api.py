'''Version 0.1'''
import json
from ingredients import ingredients
from methods import methods
from tools import tools
import scraper
from pprint import pprint

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    results = {}
    results['url'] = url

    recipe = scraper.get_recipe(url)

    unit_measure, regex = ingredients.load_ingredient_data()
    results['ingredients'] = []
    for ing in recipe['ingredients']:
        results['ingredients'].append(ingredients.parse_ingredients(ing, unit_measure, regex))

    primary_cooking_methods, methods_by_step, cooking_methods = methods.find_all_methods(recipe['title'],recipe['directions'])
    results['primary cooking method'] = primary_cooking_methods
    results['cooking methods'] = cooking_methods

    tools_by_step, all_tools = tools.find_tools(recipe['directions'])
    results['cooking tools'] = all_tools

    preptools = {'fork':['mixed'],'knife':['chopped','sliced','minced','diced'], 'grater':['grated'], 'mortar and pestle':['crushed']}
    methodtools = {'baster':['basting'], 'oven':['bake','broil'], 'fork':['mix']}

    for ingredient in results['ingredients']:
        for t in preptools:
            if ingredient['preparation'] in preptools[t]:
                results['cooking tools'].append(t)

    for method in results['cooking methods']:
        for t in methodtools:
            if method in methodtools[t]:
                results['cooking tools'].append(t)

    results['cooking tools'] = f7(results['cooking tools'])

    # pprint(results)
    
    
    # steps
    steps = []
    for (i, d) in enumerate(recipe['directions']):
        step = {}
        print "\n",d
        step_methods = methods_by_step[i]
        step_tools = tools_by_step[i]
        
        for sm in step_methods:
            for t in methodtools:
                if sm in methodtools[t] and t not in step_tools:
                    tools_by_step[i].append(t)
                    
                    
        step_ingredients = []
        for ingredient in results['ingredients']:
            ingredient_words = ingredient['name'].split()
            for w in ingredient_words:
                if w in d:
                    step_ingredients.append(ingredient['name'])
                    break
        
        step['methods'] = methods_by_step[i]
        step['tools'] = tools_by_step[i]
        step['ingredients'] = step_ingredients
        
        steps.append(step)
    
    
    return results
