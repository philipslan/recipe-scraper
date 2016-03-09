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
	entry_list_names = [nltk.pos_tag(lis,tagset='universal') for lis in preprocess(entry_list)]
	name = get_names([list(i) for e in entry_list_names for i in e])
	### Only 1 word left in list ###
	# if len(entry_list) == 1:
	# 	word = nltk.pos_tag(entry_list,tagset="universal")
	# 	if word[0][1] == "NOUN":
	# 		name = [word[0][0]]
	# ### Create Bigrams and find parts of speech that are nouns ###
	# for bigram in nltk.bigrams(entry_list):
	# 	tags = nltk.pos_tag(bigram,tagset="universal")
	# 	check_bigrams = []
	# 	for i in tags:
	# 		if i[1] == "NOUN":
	# 			check_bigrams.append(i[0])
	# 	if len(check_bigrams) == 2:
	# 		name.append(string.join(check_bigrams))
	# 	else:
	# 		if check_bigrams:
	# 			if check_bigrams[0] not in name:
	# 				name.append(check_bigrams[0])
	# 	### Unigram ###
	# 	for i in bigram:
	# 		word = nltk.pos_tag([i],tagset="universal")
	# 		if word[0][1] == "NOUN" and word[0][0] not in name:
	# 			name.append(word[0][0])
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


def get_names(clean_tags):
	print clean_tags
	print len(clean_tags)
	if len(clean_tags)==2:
		clean_tags[0][len(clean_tags[0])-1][1]="list"
		clean_tags[1][0][1]="list"
	output = []
	for tags in clean_tags:
		print tags
		for i,tag in enumerate(tags):
			if tag[1] == "NOUN":
				before = [val[0] for val in tags[:i]]
				noun = tag
				after = [val[0] for val in tags[i:]]
				output+= all_possible_combinations(tags[:i],tags[i],tags[i+1:])
				print "NEW OUTPUT: ", output
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
	print "ALL POSSIBLE COMBINATIONS\n--------------"
	print "BEFORE: ", before
	print "NOUN: ", noun
	print "AFTER: ", after
	before_li = join_lists_reverse([b[0] for b in before])
	after_li = join_lists([a[0] for a in after])
	print before_li
	print after_li
	boutput = []
	for val in before_li:
		boutput.append(val+' '+noun[0])
	output = []
	for val in after_li:
		for b in boutput:
			print b
			print val
			output.append(str(b+' '+val).strip().strip(','))
	return output

def preprocess(entry_list):
	print entry_list
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
