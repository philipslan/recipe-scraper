from scraper import get_recipe
from tools import tools

url = "http://allrecipes.com/recipe/220479/cilantro-edamame-hummus/"
recipe = get_recipe(url)

tools.find_tools(recipe['directions'])
