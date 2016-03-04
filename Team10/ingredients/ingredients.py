import json
import nltk
import string

### loading measurements ###
with open('units.json') as data_file:
	units_measure = set(json.load(data_file))

def parse_ingredients(entry):
	output = {}
	entry_list = entry.split()

	### finding quantity 	 ###
	quantity = ["0","1",None]
	for j in entry_list[0]:
		if is_number(j):
			quantity = [entry_list.pop(0)]
			break

	### finding measurement  ###
	measurement = []
	for i,val in enumerate(entry_list):
		if val in units_measure:
			measurement.append(entry_list.pop(i))
			break
	if not measurement:
		measurement = ["unit", "units","discrete"]

	### finding name 		 ###
	name = []

	### Only 1 word left in list ###
	if len(entry_list) == 1:
		word = nltk.pos_tag(entry_list,tagset="universal")
		if word[0][1] == "NOUN":
			name = [word[0][0]]

	### Create Bigrams and find parts of speech that are nouns ###
	for bigram in nltk.bigrams(entry_list):
		tags = nltk.pos_tag(bigram,tagset="universal")
		check_bigrams = []
		for i in tags:
			if i[1] == "NOUN":
				check_bigrams.append(i[0])
		if len(check_bigrams) == 2:
			name.append(string.join(check_bigrams))
		else:
			if check_bigrams:
				if check_bigrams[0] not in name:
					name.append(check_bigrams[0])
		### Unigram ###
		for i in bigram:
			word = nltk.pos_tag([i],tagset="universal")
			if word[0][1] == "NOUN" and word[0][0] not in name:
				name.append(word[0][0])

	### finding descriptor 	 ###
	output["entry"] = entry
	output["name"] = name
	output["quantity"] = quantity
	output["measurement"] = measurement
	output["descriptor"] = []
	output["preparation"] = []
	output["prep-description"] = []
	output["max"] = None

	return output

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
