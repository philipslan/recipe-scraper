
def reverser(struct):
	output = {}

	for key in struct:
		for val in struct[key]:
			if val in output:
				output[val].append(key)
			else:
				output[val]=[key]

	return output