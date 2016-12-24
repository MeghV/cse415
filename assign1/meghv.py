# bot.py
# A conversational DJ simulation modelled after
# the real world musician, DJ Khaled.

# Megh Vakharia, meghv
# 


from re import *   # Loads the regular expression module.
import random 

# Memory: Remembers that "hello" was already said and
# responds accordingly.
HELLO_SAID = False

# Introduction Words that will be considered in the rules
INTRODUCTION_INPUTS = ["hello", "hi", "yo", "hey", "hiya"]

# Introduction responses to the other converser
INTRODUCTION_RESPONSES = ["What's happenin' my homie.",
							"Whattup fam.",
							"You're here to find the major key? I got it. Welcome.",
							"You are now talking to DJ Khaled, the most smartest most loyal DJ."]

# phrases to ask the conversing bot's name
NAME_ASKS = ["What's yo name?", 
			 "Now tell me fam... What's your name?",
			 "If you loyal, you gonna tell me what you called.",
			 "I'm DJ Khaled. Who're you?",
			 "But you gotta tell me - what's yo name?"]

# No-input responses
NO_INPUT_RESPONSES = ["Yo, my ears can't hear what you're saying. Step up and speak up."
					  "You ain't gonna become a Major Key talking like that. Or I guess not talking like that.",
					  "The world ain't gonna hear you like that.",
					  "Nobody here know what your talking bout."]

# Words to indicate breaks in phrases. Used to understand
# sentences with multiple verbs.
PROGRESSION_WORDS = ["and","or", "n", "plus"]

# Used to detect whether converser is asking
# about name
NAME_PHRASES = {4: [[ "hi", "my", "name", "is"] ], 
				3: [ ["my", "name", "is"],
					 ["hi", "my", "names"],
					 ["the", "name", "is"]],
				2: [ ["my", "names"], 
					 ["the", "names"],
					 ["hi", "im"]]}

# Confirmation words within conversation
CONFIRMATION_WORDS = ["yes", "yeah", "ye", "yep", "mhm", "mhmm",
						"duh", "uhhuh", "yepyep", "yea"]

# Non-confirmation words within conversation
NEGATIVE_WORDS = ["no", "nope", "nah", "na", "nay", "negative",
						"lolno"]

# Info about the Bot that it can use when responding to
# converser.
BOT_INFO = {"name":"DJ Khaled", 
			"names": "DJ Khaled", 
			"creator": "Megh Vakharia", 
			"maker": "Megh Vakharia",
			"personality":[]}

# Maps pronouns
CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are', 'youre':'im'}

# Positive verbs
POSITIVE_PREFERENTIAL_VERBS = ["like", "love", 
								 "enjoy", "adore"]

# Negative verbs
NEGATIVE_PREFERENTIAL_VERBS = ["hate", "despise"]

# Used to punt the conversation forward
PUNTS = ['You want my advice? Don\'t play yourself.',
         'I can deal with everything. I got the answer for anything. This DJ Khaled.',
         'Smh they get mad when u have joy.',
         'ANOTHA ONE!',
         'The key is to make it. I made it. I got the key.',
         """They don't want you to win. They don't want you to have the 
         No. 1 record in the country. They don't want you get healthy. 
         They don't want you to exercise. And they don't want you to have that view."""]

# Stores information about the opponent, such as:
# name 		: opponent's name (string)
# likes 	: preferences based on preferential verbs (dict)
OPPONENT_INFO = {}

STATE = ""
PREFERENCE_STATE = ""

# Introduces the chatbot to the converser
def introduce():
    return """What's happenin'. My name is DJ Khaled and I'm the most smartest, most successful DJ on the planet. 
		   If you can't trust me, you can't trust nobody. I am the Major Key. I was programmed by Megh Vakharia. 
		   If you ain't loyal, don't talk to me, contact my creator at meghv@uw.edu."""

def agentName():
	'Returns this bot\'s name'
	return "DJ Khaled"

def RunBot():
	'RunBot is the top-level function, containing the main loop.'
	while True:
		the_input = input('TYPE HERE:>> ')
		if match('bye',the_input):
			print('Yo, until next time homie!')
			return
		respond(the_input.strip())


def respond(user_input):
	"""
	Responds to user input using numerous rules and word detectors, 
	as outlined in each rule below.
	"""
	overall_response = []
	wordlist = split(' ',remove_punctuation(user_input))
	wordlist[0] = wordlist[0].lower()
	mapped_wordlist = you_me_map(wordlist)
	mapped_wordlist[0] = mapped_wordlist[0].capitalize()
	
	global STATE # current state - used to get preference reasoning
	global PREFERENCE_STATE # the preference that is currently being discussed
	global HELLO_SAID # if hello has been already said or not

	# Non-Response Rule =================================
	# 1) User has sent nothing or has only sent punctuation
	if wordlist[0] == '':
		overall_response += [ random.choice(NO_INPUT_RESPONSES) ]
		# cycles through multple responses
	else:
		# Introduction Rules =======================================================
		# Introduction-type input of size <= 2 ("hi there", "hello!", "what's up?")
		if (len(wordlist) <= 2) and (wordlist[0] in INTRODUCTION_INPUTS):
			
			# 2) Memory Function: If the user has already said hello, we
			# already know and respond accordingly.
			if HELLO_SAID == True:
				overall_response += [ "My homie, you already told me 'hello'. We ain't on that Adele stuff, we good." ]
			else:
				overall_response += [ random.choice(INTRODUCTION_RESPONSES) ]
				# cycles through multple responses
			# 3) Memory function: We want to know the user's name, so we ask
			# them if we don't know. If the name is known, it is used.
			if 'name' not in OPPONENT_INFO:
				overall_response += [ random.choice(NAME_ASKS)] # cycles through responses
				STATE = "name_asked"
			else:
				overall_response += [ "You know you smart, " + stringify(OPPONENT_INFO['name']) +"."]
		
		# Name Getter Rules ======================================
		# Detects whether a user is saying their name.
		# 4) First two words are introductory.
		# Example: "My name's Megh" | "Hi im megh" | etc.
		elif wordlist[0:2] in NAME_PHRASES[2]:
			overall_response += nameAskCheck(wordlist, 0,2)
			wordlist = wordlist[2:]
		
		# 5) First three words are introductory.
		# Example: "My name is Megh" | "Hi i am megh" | etc.
		elif wordlist[0:3] in NAME_PHRASES[3]:
			overall_response += nameAskCheck(wordlist, 0,3)
			wordlist = wordlist[3:]
		
		# 6) First four words are introductory.
		# Example: "Hi my name is Megh"
		elif wordlist[0:4] in NAME_PHRASES[4]:
			overall_response += nameAskCheck(wordlist, 0,4)
			wordlist = wordlist[4:]
		
		# Preference Clarification Rules ==========================
		# This STATE occurs when the converser is being asked to
		# explain why they like something.
		elif STATE == "preference_clarification":
			
			# 7) Memory function: Stores the reasoning for the preference.
			if "because" in wordlist:
				index = wordlist.index("because")
				preference_reasoning = stringify(wordlist[index + 1:])
				mapped_wordlist = you_me_map(wordlist)
				addPositivePreferenceReasoningToOpponent(PREFERENCE_STATE, preference_reasoning)
				overall_response += ["I gotchu, you like " + PREFERENCE_STATE + " " + stringify(mapped_wordlist) + "? We good here."]
				STATE = ""
			else:
				overall_response += ["You gotta specify. Why you like " + PREFERENCE_STATE]		
		else:
			# eliminate "and" if still present 
			# so we can process next phrase
			if wordlist[0] in PROGRESSION_WORDS:
				wordlist = wordlist[1:]
			mapped_wordlist = you_me_map(wordlist)
			
			# Positive Preferences Rules ======================================
			# 8) Checks if the first two words are preference verbs and stores
			# user's preferences.
			if (len(wordlist) > 1 and wordlist[0] == "i" and  wordlist[1] in POSITIVE_PREFERENTIAL_VERBS)	:
				mapped_wordlist = you_me_map(wordlist)
				preference = wordlist[2]
				addPositivePreferenceKeyToOpponent(preference)
				overall_response += ["Why do " + stringify(mapped_wordlist) + "?"]
				PREFERENCE_STATE = preference
				STATE = "preference_clarification"
			else: 

				# General Phrase Rules ========================================
				# 9)
				if wordlist[0:3] == ['do','you','think']:
					options = ["I'm DJ Khaled, I got my own opinions but to be a Major Key you gotta answer your own. I can't help you.",
						  		"You askin' me something crazy cuz I think a lot of things. Why do you think " + stringify(you_me_map(wordlist[3:])) + "." ]
					overall_response += [ random.choice(options) ]
				# 10)
				if wordlist[0:2] == ['i','am']:
					overall_response += ["I'm all ears always fam. Why is you " + stringify(mapped_wordlist[2:]) + '.']
				# 11)
				if wordlist[0:2] == ['i','have']:
					overall_response += ["Dang, how long you had that " + stringify(mapped_wordlist[2:]) + '...?']
				# 12)
				if wordlist[0:2] == ['i','feel']:
					overall_response += ["Check it, I feel that way too homie."]
				# 13) Memory function: If the converser proclaims that the bot is something ("you are"),
				# the proclamation is stored for future user
				if wordlist[0:2] == ['you','are']:
					existing_personalities = getBotPersonality()
					if len(existing_personalities)  < 1:
						overall_response += ["My homie, I'm not sure why you'd say I'm " + stringify(mapped_wordlist[2:]) + ', but I noted it']
						
					else:
						overall_response += ["You know I'm " + stringify(mapped_wordlist[2:]) + '. I\'m also ' + random.choice(existing_personalities)]
					addToBotPersonality(stringify(mapped_wordlist[2:]))
				# 14)
				if verbp(wordlist[0]):
					overall_response += ["Why you want me to " + stringify(mapped_wordlist) + '?']
				# 15)
				if wordlist[0:2]==['can','you'] or wordlist[0:2]==['could','you']:
					overall_response += ["Bruh, that's some talk about " + wordlist[0] + ' ' + stringify(mapped_wordlist[2:]) + '.']
				# 16) Sentences begin with positive or negative words (yes, no)
				if wordlist[0] in NEGATIVE_WORDS or wordlist[0] in POSITIVE_PREFERENTIAL_VERBS:
					overall_response += ["You feel how you feel mah homie. I'm wit it."]
				# Preference Response rules ========================================
				# if the phrase begins with "do you like", the first word is
				# used to determine questioning purpose and the following words
				# are used to determine subject
				if wordlist[0:2] == ["what", "is"] or wordlist[0:1] == ["whats"]:
					# if it is a personal question, resort
					# to personal info
					if 'whats' == wordlist[0]:
						start_index = 1
					elif 'what' == wordlist[0]:
						start_index = 2

					# 17) Memory function: Based on what the converser is asking,
					# this bot may respond with its own info.
					if wordlist[start_index] == "your":
						if len(wordlist) > start_index+1:
							subject = stringify(wordlist[start_index+1:])
							if subject in BOT_INFO.keys():
								overall_response += [ "Yo, my " + subject + " is " + BOT_INFO[subject] + "."]
							else:
								mapped_wordlist = you_me_map(wordlist)
								overall_response += [ stringify(mapped_wordlist) + "? Take a guess fam."]

							if subject in OPPONENT_INFO.keys():
								overall_response += [ "And I know yo " + subject + " is " + stringify(OPPONENT_INFO[subject])]
							else:
								overall_response += [ "What's your " + subject + " fam?"]
							
					# 18) Memory function: Based on what the converser is asking,
					# this bot may respond with stored info about the bot.
					elif wordlist[start_index] == "my":
						if len(wordlist) > start_index+1:
							subject = stringify(wordlist[start_index+1:])
							if subject in OPPONENT_INFO.keys():
								overall_response += [ "Yo, yo " + subject + " is " + OPPONENT_INFO[subject] + ". You already told me that tho!"]
							else:
								mapped_wordlist = you_me_map(wordlist)
								overall_response += [ stringify(mapped_wordlist) + "? You tell me fam."]
				# 19)
				if wpred(wordlist[0]):
					overall_response += [ "I don't answer no questions like that. You tell me " + wordlist[0] +"."]
				# 20) Memory function: If converser is asking about Bot's preferences, preferences are created
				# and returned.
				if wordlist[0:3] == ["do", "you", "like"] or wordlist[0:4] == ["what","do", "you", "like"]:
					# do you like ....
					# determine if question is directed
					what_question = True if wordlist[0] == "what" else False

					if what_question:
						subject = wordlist[4:] if len(wordlist) > 4 else None
					else:
						subject = wordlist[3:] if len(wordlist) > 3 else None

					# determine if a subject exists:
					resp = ""
					if subject == None:
						if what_question:
							overall_response += [ "What do I like about what?" ]
						else:
							overall_response += [ "Do I like what?" ]
					else:
						if what_question:
							# what do you like about []
							if subject[0] == "about":
								subject = stringify(subject[1:])
								addPositivePreferenceKeyToSelf(subject)
								overall_response += [ "What do YOU like about " + subject + "?" ]

							else:
							# what do you like []??
								overall_response += ["About what?"]
						else:
							# do you like [subject]
							subject = stringify(subject)
							addPositivePreferenceKeyToSelf(subject)
							overall_response += [ "Oh absolutely, I " + random.choice(POSITIVE_PREFERENTIAL_VERBS) + " " + subject + "."]
							if opponentHasPositivePreference(subject):
								overall_response += [ "I know you like " + subject + " too, right ;)?" ]
					
			
				# 21)
				if 'major key' in wordlist:
					overall_response += ["You got it with that major key talk. You mah homie now."]
				# 22)
				elif 'da best' in wordlist:
					overall_response += ["You da best, we da best, everyone's da best. We good."]
				# 23)
				elif 'changed a lot' in wordlist:
					overall_response += ["We all changed a lot. The world is changin' just like you and me. We good out here."]

				if len(overall_response) == 0:
					overall_response += [ punt() ]
	# Debug: print(' '.join(overall_response))
	return ' '.join(overall_response)

def nameAskCheck(wordlist, indexStart,indexEnd):
	"""
	Checks if the wordlist contains the user's name between the given range.
	If it does, the bot acts accordingly (storing name, clarifying name, or asking name).
	"""
	overall_response = []
	if not (len(wordlist) >= indexEnd+1):
		overall_response += ["I don't know why you playin, but what's yo name?"]
		STATE = "name_asked"
	else: 
		STATE = ""
		name = wordlist[indexEnd:indexEnd+1]
		if 'name' not in OPPONENT_INFO:
			addNameToOpponent(name)
			overall_response += ["Yo, " + stringify(name) + ", nice to meet ya fam."]
		elif name == OPPONENT_INFO['name']:
			overall_response += ["Why you sayin' yo name, I gotchu you already on my list.."]
		else: 
			overall_response += [ "You playin' with me? You told me yo name was " + \
			stringify(OPPONENT_INFO['name']) + ". I trust you though, so I'll call you " + \
			stringify(name) + "."]
			addNameToOpponent(wordlist[indexEnd:indexEnd+1])
		wordlist = wordlist[indexEnd+1:]
	return overall_response

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:|\'") 
def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

def opponentHasPositivePreference(preferenceToCheck):
	'Checks whether an opponent has the preference.'
	if 'likes' in OPPONENT_INFO \
		and preferenceToCheck in OPPONENT_INFO['likes']:
		return OPPONENT_INFO['likes'][preferenceToCheck]
	else:
		return False

def getBotPersonality():
	'Returns all values within the bot\'s personality'
	if 'personality' not in BOT_INFO:
		BOT_INFO['personality'] = []
	return BOT_INFO['personality']

def addToBotPersonality(personality_string):
	"""
	Stores information about this bot\'s personality based on 
	"you are" queries.
	"""
	if 'personality' not in BOT_INFO:
		BOT_INFO['personality'] = []
	BOT_INFO['personality'].append(personality_string)	
	return personality_string

def addNameToOpponent(name):
	'Stores the conversing bot\'s stated name.'
	OPPONENT_INFO['name'] = name

def addPositivePreferenceKeyToOpponent(input):
	'Stores a new prefernce to the conversing bot.'
	if 'likes' not in OPPONENT_INFO:
		OPPONENT_INFO['likes'] = {}
	OPPONENT_INFO['likes'][input] = ""

def addPositivePreferenceReasoningToOpponent(preference, reasoning):
	"""
	Stores a reasoning to an existing preference OR 
	creates the preference : reasoning mapping
	"""
	if 'likes' not in OPPONENT_INFO:
		OPPONENT_INFO['likes'] = {}
	OPPONENT_INFO['likes'][preference] = reasoning

def addPositivePreferenceKeyToSelf(input):
	'Stores a new prefernce to this bot.'
	if 'likes' not in BOT_INFO:
		BOT_INFO['likes'] = {}
	BOT_INFO['likes'][input] = ""

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]



