from Team10 import recipe_api
from pprint import pprint
import Team10.scraper
from Team10.transformations.transformations import *

recipe = (Team10.scraper.get_recipe("http://allrecipes.com/recipe/45696/da-beef-lovers-half-time-stuffed-meatloaf/?internalSource=staff%20pick&referringId=256&referringContentType=recipe%20hub"))

if is_category('vegan',recipe['ingredients'],recipe['title']) == False:
	pprint(transform(recipe,"vegan","to"))
else:
	pprint(transform(recipe,"vegan","from"))
