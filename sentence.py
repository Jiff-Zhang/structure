from word import Word
class Sentence(object):
	"""class Sentence is used to help us describe the structure of sentence,
	each sentence consists of some word in order,
	for each word, we will describe the 'txt', 'pos' and 'rhythm' components,
	for more information, you can refer to 'word.py'"""
	def __init__(self):
		self.sentence=[]

	def append(self,new_word):
		"""This function is used to append a word to the tail of a sentence."""
		self.sentence.append(new_word)

	def append(self,txt,pos,rhythm):
		"""This function is used to append a word (still component) to the tail of a sentence."""
		self.sentence.append(Word(txt,pos,rhythm))

	def show(self):
		"""This function is used to show how a sentence looks like."""
		for word in self.sentence:
			#print "<word>%(txt)s_%(pos)s%(rhythm)s<\word>"%word.word
			print "%(txt)s_%(pos)s%(rhythm)s"%word.word,
		
		print

	def length(self):
		"""This function is used to show the length of the sentence.
		How many words are in this sentence?"""
		return len(self.sentence)
