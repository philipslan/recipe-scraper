from BeautifulSoup import BeautifulSoup
import urllib


def get_recipe(url):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)

    o = {'ingredients':[],'directions':[]}
    o['ingredients'] = [ingredient.text for ingredient in soup.findAll("span", {"itemprop":"ingredients"})]
    o['directions'] = [direction.text for direction in soup.findAll("span",{"class":"recipe-directions__list--item"})]
    
    return o