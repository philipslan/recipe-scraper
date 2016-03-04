import json
import nltk

with open('units.json') as data_file:
	units_measure = set(json.load(data_file))

def parse_ingredients(entry):
	### loading measurements ###
	

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
	for bigram in nltk.bigrams(entry_list):
		tags = nltk.pos_tag(bigram,tagset="universal")
		for entry in tags:
			### THIS IS MESSED UP FIX IT BRO ####
			if entry[1] == "NOUN": name.append(entry[0])
				  
			
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
