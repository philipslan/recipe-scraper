import json
import nltk
import string
import re
import os
path = os.path.dirname(__file__)

### loading measurements ###
def load_ingredient_data():
	with open(os.path.join(path,'units.json')) as data_file:
		units_measure = set(json.load(data_file))
	with open(os.path.join(path,'prep_methods.json')) as data_file:
		prep_methods = json.load(data_file)
	regex = ""
	for i,method in enumerate(prep_methods):
		regex += method + "\w+|" + method if i is len(prep_methods) - 1 else method + "\w+|" + method + "|"
	return units_measure, regex

def parse_ingredients(entry, units_measure, prep_regex):
	output = {}
	entry_list = entry.split()
	### finding quantity 	 ###
	quantity = "0"
	for j in entry_list[0]:
		if is_number(j):
			quantity = entry_list.pop(0)
			break
	### finding measurement  ###
	measurement = ''
	for i,val in enumerate(entry_list):
		if val in units_measure:
			measurement= entry_list.pop(i)
			break
	if not measurement:
		measurement = "units"
	### finding name 		 ###
	name = " ".join(entry_list)
	entry_list_names = [nltk.pos_tag(lis,tagset='universal') for lis in preprocess(entry_list)]
	names_long = get_names([[list(i) for i in e] for e in entry_list_names])
	### finding descriptor 	 ###
	descriptor = get_desc(names_long)
	### finding preparation  ###
	preparation = get_prep(entry_list, prep_regex)
	output["name"] = name
	output["quantity"] = quantity
	output["measurement"] = measurement
	output["descriptor"] = descriptor
	output["preparation"] = preparation
	output["prep-description"] = "none"
	return output

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_names(clean_tags):
	if len(clean_tags)==2:
		clean_tags[0][len(clean_tags[0])-1][1]="list"
		clean_tags[1][0][1]="list"
	output = []
	for tags in clean_tags:
		for i,tag in enumerate(tags):
			if tag[1] == "NOUN":
				before = [val[0] for val in tags[:i]]
				noun = tag
				after = [val[0] for val in tags[i:]]
				output+= all_possible_combinations(tags[:i],tags[i],tags[i+1:])
	if output:
		return list(set(output))
	return [' '.join([t[0] for t in tags])]

def join_lists(li):
	output = ['']
	for i in xrange(len(li)):
		output.append(' '.join(li[:i+1]))
	if output:
		return output
	return ['']

def join_lists_reverse(li):
	output = ['']
	for i in xrange(len(li)):
		output.append(' '.join(li[i:]))
	if output:
		return output
	return ['']

def all_possible_combinations(before, noun, after):
	before_li = join_lists_reverse([b[0] for b in before])
	after_li = join_lists([a[0] for a in after])
	boutput = []
	for val in before_li:
		boutput.append(val+' '+noun[0])
	output = []
	for val in after_li:
		for b in boutput:
			output.append(str(b+' '+val).strip().strip(','))
	return output

def preprocess(entry_list):
	output_before = []
	output_after = []
	for i,val in enumerate(entry_list):
		if val.find(',') != -1:
			output_before = entry_list[:i+1]
			output_before.append(' '.join(entry_list[i+1:]))
			output_after.append(' '.join(entry_list[:i+1]))
			output_after += entry_list[i+1:]
			return [output_before,output_after]
	return [entry_list]

def get_prep(entry_list, prep_regex):
	if len(entry_list) == 1:
		return "none"
	else:
		tag_list = []
		for word in entry_list:
			prep = re.findall(prep_regex,word)
			if prep:
				return prep[0]
		return "none"

def get_desc(names):
	if len(names) == 1:
		return "none"
	else:
		array = []
		for x in names:
			index = x.find(",")
			if index != -1:
				x = x[:index]+x[index+1:]
			array.extend(x.split())
		freqdist = nltk.FreqDist(array).most_common(50)
		margin = freqdist[0][1]
		for item in freqdist:
			if item[1] != margin:
				return item[0]
		return "none"
		# regex = ''
		# for i,desc in enumerate(not_descriptor):
		# 	if i == len(not_descriptor) - 1:
		# 		regex += desc + " | " + desc + "|" + desc 
		# 	else:
		# 		desc + " | " + desc + "|" + desc + "|"
		# all_desc = set()
		# for name in names:
		# 	if re.sub(regex,"",name):
		# 		all_desc.add(re.sub(regex,"",name))
		# for desc in all_desc:
		# 	if desc[0] == ",":
		# 		all_desc.remove(desc)
		# 		all_desc.add(desc[2:])
		# return list(all_desc)