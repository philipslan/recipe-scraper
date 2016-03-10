from scraper import get_recipe
from tools import tools

url = "http://allrecipes.com/Recipe/Baked-Lemon-Chicken-with-Mushroom-Sauce/"
recipe = get_recipe(url)

tools.find_tools(recipe['directions'])
