from flask import Flask, render_template, jsonify, request
import urllib
import recipe_api
from recipe_api import *
import transformations.transformations
from transformations.transformations import *
import scraper
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/_recipe_scraper/<path:url>')
def get_recipe(url):
    output = parse_recipe_from_url(url)
    recipe = scraper.get_recipe(url)
    ingredients = recipe['ingredients']
    title = recipe['title']

    output['vegetarian'] = is_category('vegetarian',ingredients,title)
    output['vegan'] = is_category('vegan',ingredients,title)
    output['low_carb'] = is_category('low-carb',ingredients,title)
    output['low_sodium'] = is_category('low-sodium',ingredients,title)
    output['chinese'] = is_category('chinese',ingredients,title)
    output['italian'] = is_category('italian',ingredients,title)
    if output['vegan']:
        output['vegetarian'] = True
    return jsonify(output)

@app.route('/_transform/<path:url>/<to_or_from>/<category>')
def transform(url, to_or_from, category):
    recipe = scraper.get_recipe(url)
    tr = transformations.transformations.transform(recipe, category, to_or_from)
    results = {}
    output = parse_recipe(tr)

    ingredients = tr['ingredients']
    title = tr['title']
    output['vegetarian'] = is_category('vegetarian',ingredients,title)
    output['vegan'] = is_category('vegan',ingredients,title)
    output['low_carb'] = is_category('low-carb',ingredients,title)
    output['low_sodium'] = is_category('low-sodium',ingredients,title)
    output['chinese'] = is_category('chinese',ingredients,title)
    output['italian'] = is_category('italian',ingredients,title)
    output[category] = to_or_from == 'to'
    if output['vegan']:
        output['vegetarian'] = True
    return jsonify(output)


if __name__ == "__main__":
	app.run()
