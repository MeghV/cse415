# agent.py
# Ryan Chui
# 1234808
# CSE 415 - Assignment 1
# 
# This program is a chatterbot which can converse based on what the user inputs.

import re
import random

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

PUNTS = ["Lana. LANA. LAAAAAAAANNNNNAAAAAAAAAAAA",
         "I bought a t-shirt once that said 'Female Body Inspector'.",
         "I told Woodhouse to buy lemoncurd. Now what do I spread on my toast? Tears?",
         "I'm not saying I invented the turtleneck, but I was the first person to realize its \
potential as a tactical garment. The tactical turtleneck! The... tactleneck.",
         "I'm scared if I stop drinking all at once, the cumulative hangover will literally \
kill me.",
         "Lying is like 95% of what I do."]

CHANGE = ["Are you kidding? Dude. Bros before apparent threats to national security.", 
		  "Something, something. danger zone! I know. I'm not even trying anymore."]

QUOTE = ["'The best way to predict the future is to create it.'",
		 "'If today was the last day of your life, would you want to do what you are abou to \
do today?'",
		 "'Freedom is not worth having if it does not include the freedom to make mistakes.'"]

punctuation_pattern = re.compile(r"\,|\.|\?|\!|\;|\:")

punt_count = 0
punt_size = 6
change_count = 0

# Intoduces the chatterbot to the user.
def introduce():
	return"""My name is Sterling Malory Archer, a secret agent codename: 'Duchess'. 
I was programmed by Ryan Chui. If you don't like the DANGER ZONE, 
contact him at rchui@u.washington.edu. 
Psych! I have no idea who that guy is. What's up?"""

# Provides responses to the inputs given by the user.
# Parameters: inputString - string used to determine response.
def respond(inputString):
	# Contains "bye"
	if re.match("bye", inputString):
		return "Goodbye"
	wordlist = remove_punctuation(inputString).split(" ")
	wordlist[0] = wordlist[0].lower()
	mapped_wordlist = you_me_map(wordlist)
	mapped_wordlist[0] = mapped_wordlist[0].capitalize()
	# Contains nothing
	if wordlist[0] == "":
		return ("Your silence is like rubbing a cheese gratter on my brain.")
	# Starts with "I am"
	if wordlist[0:2] == ["i", "am"]:
		return "I know why you are " + stringify(mapped_wordlist[2:]) +\
			   ". You don't need to tell me. I'm a secret agent remember?"
	# Contains words Burt and Reynolds
	if 'Burt' in wordlist and 'Reynolds' in wordlist:
		return "Oh my god. Burt Reynolds is my idol!"
	# Contains word gator
	if 'gator' in wordlist:
		return "Have you seen Gator? Burt Reynolds was amazing in it."
	# Contains word zone
	if "zone" in wordlist:
		return "You know what zone we're about to enter? THE DANGER ZONE"
	# Contains word ants
	if "ants" in wordlist:
		return "Do you want ants? Because thats how you get ants."
	# Starts with "I have"
	if wordlist[0:2] == ["i", "have"]:
		return "Do you know what I have? A raging hangover."
	# Starts with "You are"
	# Memorizes the topic and stores it for use in a future punt.
	if wordlist[0:2] == ["you", "are"]:
		PUNTS.append("So tell me again how I am " + stringify(mapped_wordlist[2:]) + ".")
		global punt_size
		punt_size += 1
		return "Oh you think I am " + stringify(mapped_wordlist[2:]) + "? Tell me more."
	# Starts with "I think"
	if wordlist[0:2] == ["i", "think"]:
		return "Is that what you think? Are you going to think that you're people next?"
	# Starts with "why"
	if wordlist[0] == "why":
		return "If I knew the answer, we wouldn't still be talking."
	# Starts with "Do you think"
	if wordlist[0:3] == ["do", "you", "think"]:
		return "I think that Woodhouse is taking his sweet time with my mojitos."
	# Starts with a verb
	if verbp(wordlist[0]):
		return "Sounds like a trap."
	# Contains "yes"
	if "yes" in wordlist:
		return "That's the spirit!"
	# Contains "no"
	if "no" in wordlist:
		return "Do you want to continue to think about that?"
	# Contains "mother"
	if "mother" in wordlist:
		return "How do you know my mother? Is she here?"
	# Starts with "how"
	if wordlist[0] == "how":
		return quote()
	# First or second word is "what"
	if wordlist[0] == "what":
		return change()
	# Punts 
	return punt()

# Randomly returns a stored quote.
def quote():
	return "Someone once said, " + random.choice(QUOTE)

# Returns a statement that changes to attempt to change the subject.
def change():
	global change_count
	change_count += 1
	return CHANGE[change_count % 2]

# Compares an input with the list of stored verbs.
def verbp(w):
	return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

# Takes list of input words and concatenates them together.
def stringify(wordlist):
	return " ".join(wordlist)

# Removes all punctuation from the input
def remove_punctuation(text):
	return re.sub(punctuation_pattern, "", text)

# Returns a rotating statement if nothing inputted is recognized.
def punt():
	global punt_count
	punt_count += 1
	return PUNTS[punt_count % punt_size]

# Returns chatterbot nickname.
def agentName():
	return "Archer"

# Takes input words and changes all "you" to "me"
def you_me_map(wordlist):
	return [you_me(i) for i in wordlist]

# Changes all "you" to "me"
def you_me(i):
	try:
		result = CASE_MAP[i]
	except KeyError:
		result = i
	return result














