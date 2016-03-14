from flask import Flask, render_template, jsonify, request
import urllib
import Team10.recipe_api
from Team10.recipe_api import *
import Team10.transformations.transformations
from Team10.transformations.transformations import *
import Team10.scraper

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/_recipe_scraper/<path:url>')
def get_recipe(url):
    output = parse_recipe(url)
    print "output"
    recipe = Team10.scraper.get_recipe(url)
    ingredients = recipe['ingredients']
    title = recipe['title']

    output['vegetarian'] = is_category('vegetarian',ingredients,title)
    output['vegan'] = is_category('vegan',ingredients,title)
    output['low_carb'] = is_category('low-carb',ingredients,title)
    output['low_sodium'] = is_category('low-sodium',ingredients,title)
    return jsonify(output)
    
# @app.route('/_get_year/<year>')
# def get_year(year):
# 	get_tweets(year)
# 	return jsonify(result=True)

# @app.route('/_run_category')
# def run_category():
# 	year = request.args.get('year', 0, type=str)
# 	category = request.args.get('category', 0, type=str)
# 	return jsonify(result= getattr(gg_api, 'get_%s' % category)(year))

# @app.route('/_red_carpet')
# def _red_carpet():
# 	year = request.args.get('year', 0, type=str)
# 	typ = request.args.get('typ', 0, type=str)
# 	if typ != 'discussed':
# 		r = red_carpet(year, typ)
# 		for i in r:
# 			i[3] = list(i[3])
# 			i[4] = list(i[4])
# 		return jsonify(result=r)
# 	else:
# 		return jsonify(result=red_carpet(year, typ))
	

if __name__ == "__main__":
	app.run()
