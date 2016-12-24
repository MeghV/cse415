# 1. three_x_cubed_plus_5(2) -> 29
def three_x_cubed_plus_5(x):
	return 3 * (x ** 3) + 5

# 2. mystery_code("abc Iz th1s Secure? n0, no, 9!", 17) -> 
#	"RST zQ KY1J jVTLIV? E0, EF, 9!"
def mystery_code(str, transition):
	new_str = ''
	for c in str:
		if c.isalpha():
			if c.islower():
				topOrd = ord('z')
				bottomOrd = ord('a')
				oppositeOperator = lambda x: x.upper()
			else:
				topOrd = ord('Z')
				bottomOrd = ord('A')
				oppositeOperator = lambda x: x.lower()
			total = ord(c) + transition
			if(total > topOrd):
				new_total = bottomOrd + ( total % topOrd ) - 1
			else:
				new_total = total
			updatedC = oppositeOperator(chr(new_total))
		else:
			updatedC = c
		new_str += updatedC
	return new_str

# 3. quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1])  ->  
#	[[2, 5, 1.5, 100], [3, 8, 7, 1], [1]]
def quadruples(input):
	new_list = []
	full_lists = len(input) // 4
	for i in range(0, full_lists ):
		sublist = input[i*4: i*4 + 4]
		new_list += [sublist]
	input = input[full_lists*4:]
	if len(input) > 0:
		new_list += [input]
	return new_list

# 4. past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat']) ->
#  ['programmed', 'debugged', 'executed', 'crashed', 'repeated', 'ate']
def past_tense(word_list):
	new_list = []
	for word in word_list:
		if word == "have":
			word = "had"
		elif word == "be":
			word = "been"
		elif word == "eat":
			word = "ate"
		elif word == "go":
			word = "went"
		elif word[-1] == "e":
			word = word + "d"
		elif word[-1] == "y" and word[-2] not in ['a','e','i','o','u']:
			word = word[:-1] + "ied"
		elif word[-2] in  ['a','e','i','o','u'] and \
			word[-1] not in ['a','e','i','o','u'] and \
			word[-3] not in ['a','e','i','o','u']:
			last_consonant = word[-1:]
			word = word + last_consonant + "ed"
		else:
			word = word + "ed"
		new_list.append(word)
	return new_list





