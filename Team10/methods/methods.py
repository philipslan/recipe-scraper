import json
import nltk
import string

# loading primary methods
with open('methods/primary_methods.json') as data_file:
	primary_methods = set(json.load(data_file))

# loading secondary methods
with open('methods/cooking_methods.json') as data_file:
	methods = set(json.load(data_file))

# For methods, there is one primary cooking method (if exists) and other methods.

# When we get a list of steps, we feed each step into 'find_methods' to get
# a list of methods for each step. Combine all the methods for all the methods
# in the recipe

# To identify primary, we look for one in title.
# If doesn't exist, look in the list of methods for each step to find primary.
# Use the most frequent primary method as the primary method for the recipe.


def find_methods(step):
	"""
	input
	------
	step: a step from the directions

	output
	------
	cooking_methods: a set of 1+ method(s) that is present in the entry
	"""

	cooking_methods = []
	exclude = set(string.punctuation)
	exclude.remove('-')
	step_words = (''.join(ch for ch in step if ch not in exclude)).lower().split(' ')
	print step_words
	# find methods
	for word in step_words:
		if word in methods:
			print word
			cooking_methods.append(word)

	return list(set(cooking_methods))

def find_all_methods(title, directions):
	"""
	input
	------
	title: the title of the recipe
	directions: a list of steps

	output
	______
	primary_method: the one and only primary cooking method
	cooking_methods: other cooking methods found in the directions
	"""

	primary_method = ""
	cooking_methods = []

	# acquire all the cooking methods present in the directions (may have repeated ones)
	for step in directions:
		cooking_methods.extend(find_methods(step))

	title = title.lower().split(' ')
	for word in title:
		if word in primary_methods:
			primary_method = word

	# if we can't find the primary method in the title
	if not primary_method:
		# make nltk FreqDist to get the most frequent methods
		freq_dist = nltk.FreqDist(cooking_methods)
		most_common_methods = freq_dist.most_common(40)
		for method, freq in most_common_methods:
			if method in primary_methods:
				primary_method = method
				break

	return primary_method, list(set(cooking_methods))


