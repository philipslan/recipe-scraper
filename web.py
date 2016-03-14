from flask import Flask, render_template, jsonify, request
import urllib
import Team10.recipe_api
from Team10.recipe_api import *

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/_recipe_scraper/<path:url>')
def get_recipe(url):
    output = jsonify(parse_recipe(url))
    return output
    
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
