from scraper import get_recipe
from tools import tools

url = "http://allrecipes.com/recipe/13566/cranberry-nut-bread-i/"
recipe = get_recipe(url)

tools.find_tools(recipe['directions'])
