# -- encoding:utf-8 --
class Word(object):
	"""class Word is used to help us describe the structure of word, for example:
	as for word "提出", we will describe the txt("提出"), pos('v') and the rhythm(maybe "#1", which is determined according to the whole sentence)."""
	def __init__(self):
		self.word={'txt':'','pos':'','rhythm':''}

	def __init__(self,txt,pos,rhythm):
		self.word={'txt':txt,'pos':pos,'rhythm':rhythm}

	def set_txt(self,txt):
		"""This function is used to set the component 'txt'"""
		self.word['txt']=txt

	def get_txt(self):
		"""This function is used to get the component 'txt'"""
		return self.word['txt']

	def set_pos(self,pos):
		"""This function is used to set the component 'pos'"""
		self.word['pos']=pos

	def get_pos(self):
		"""This function is used to get the component 'pos'"""
		return self.word['pos']

	def set_rhythm(self,rhythm):
		"""This function is used to set the component 'rhythm'"""
		self.word['rhythm']=rhythm

	def get_rhythm(self):
		"""This function is used to get the component 'rhythm'"""
		return self.word['rhythm']
