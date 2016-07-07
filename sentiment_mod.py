import string
import re
import nltk
from nltk.corpus import stopwords
import nltk.tag, nltk.data
import shlex
from nltk.stem import WordNetLemmatizer
import yaml

class PreprocessSentence(object):
	def __init__(self):
		pass

	def removeArgs(self, sentence):
	# Remove arguements from the sentence
		matches=re.findall(r'\"(.+?)\"',sentence)
		for match in matches:
			sentence = sentence.replace(match,"")
		sentence = sentence.replace("\"","")
		sentence = sentence.replace("\'","")
		return sentence

	def tokenize(self, sentence):
	# Tokenize the sentence 
		sentence = self.removeArgs(sentence.lower())
		tokens = nltk.word_tokenize(sentence)
		return tokens


# preprocess("this is a simpler sentence with \"quotes\"")

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def print_dict(self):
    	print self.dictionary

    def tag_dict(self, tokens):
    	
    	tag_tokens = []
    	#print tokens
    	for token in tokens:
    		#print token
    		if token in self.dictionary.keys():
    			tag_tokens.append((token, self.dictionary[token]))
    		else:
    			tag_tokens.append((token, None))

   	return tag_tokens


def getValue(aux):
	#print aux
	if aux is None:
		return 1
	elif 'inc' in aux:
		return 2
	elif 'dec' in aux:
		return 0.5
	elif 'inv' in aux:
		return 0
	else:
		return 1


def sentimentScore(tokens):
	sent = {'imp': 0, 'urg': 0, 'flat': 0}
	for i in range(len(tokens)):
		if tokens[i][1] is None:
			continue
		else:
			emotions = tokens[i][1]
			for emo in emotions:
				#print emo
				if emo == 'important':
					sent['imp'] += getValue(tokens[i-1][1])
				elif emo == 'urgent':
					sent['urg'] += getValue(tokens[i-1][1])
				elif emo == 'flat':
					sent['flat'] += getValue(tokens[i-1][1])
	return sent




pre = PreprocessSentence()
dic = DictionaryTagger(['dicts/imp.yml', 'dicts/urg.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml', 'dicts/flat.yml'])

def sentiment(sentence):
	t = pre.tokenize(sentence)
	#dic.print_dict()
	tokens = dic.tag_dict(t)
	#print tokens
	return sentimentScore(tokens)

sent = raw_input("Enter: ")
print sentiment(sent)
