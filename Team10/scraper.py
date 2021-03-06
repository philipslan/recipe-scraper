from BeautifulSoup import BeautifulSoup
import urllib


def get_recipe(url):
    try:
    	r = urllib.urlopen(url).read()
    except:
    	return None
    soup = BeautifulSoup(r)
    o = {'title':'','imageUrl':'','ingredients':[],'directions':[]}
    o['title'] = soup.find("h1", {"itemprop":"name"}).text
    o['imageUrl'] = soup.find("img", {'class':"rec-photo"})['src']
    o['ingredients'] = [ingredient.text for ingredient in soup.findAll("span", {"itemprop":"ingredients"})]
    o['directions'] = [direction.text for direction in soup.findAll("span",{"class":"recipe-directions__list--item"}) if len(direction) > 0]
    return o