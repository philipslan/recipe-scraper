'''Version 0.1'''
from ingredients import ingredients
from methods import methods
from tools import tools
import scraper

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

    primary_cooking_methods, cooking_methods = methods.find_all_methods(recipe['title'],recipe['ingredients'])
    results['primary cooking method'] = primary_cooking_methods
    results['cooking methods'] = cooking_methods

    results['cooking tools'] = tools.find_tools(recipe['directions'])
    
    return results