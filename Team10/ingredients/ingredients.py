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
	if "/" in quantity:
		temp = quantity.split("/")
		quantity = float(temp[0]) / float(temp[1])
	else:
		quantity = int(quantity)
	### finding measurement  ###
	measurement = ''
	for i,val in enumerate(entry_list):
		if val in units_measure:
			measurement= entry_list.pop(i)
			break
	if not measurement:
		measurement = "units"
	### finding name 		 ###
	preproc_entry_list = preprocess(entry_list)
	entry_list_names = [nltk.pos_tag(lis,tagset='universal') for lis in preproc_entry_list]
	names_long = get_names([[list(i) for i in e] for e in entry_list_names])
	name,descriptor = get_name(preproc_entry_list)
	### finding descriptor 	 ###
	#descriptor = get_desc(names_long)
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

def get_name(in_list):
	if len(in_list) == 1:
		lis = in_list[0]
	else:
		lis = in_list[0][:len(in_list[0])-1]
	temp = nltk.pos_tag(lis,tagset="universal")
	output_list1 = []
	output_list2 = []

	for val in temp:
		if val[1] == 'ADP':
			break
		elif val[1] != 'VERB' and val[1] != 'PRT' and val[1] != 'ADJ' and val[1] != 'NUM':
			output_list1.append(val[0])
		elif val[1] != 'NUM':
			output_list2.append(val)

	if output_list1:
		output1 = ' '.join(output_list1).strip().strip(',')
	elif len(lis) <= 2:
		output1 =  ' '.join(lis).strip().strip(',')
	else:
		output1 = ' '.join(lis).strip().strip(',')

	for val in output_list2:
		if val[1] != 'NUM':
			output2 = val[0]

	if output_list2:
		return output1,output_list2[0][0].strip().strip(',')
	for val in temp:
		if val[1]!= 'NUM':
			return output1,val[0].strip().strip(',')



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

def parse_name(entry_list):
	return [i for i in entry_list if "/" not in i]