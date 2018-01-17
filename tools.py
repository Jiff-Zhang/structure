def sep_syllable(syllable,mode=0):
	"""this function is used to seperate the consonant with vowel and tone.
	for example:
	as for 'xvan4','x' repesents consonant, 'van' repesents vowel and '4' repesents tone.
	so if we use paramemter 'mode' for different format, which is default set as 0
	mode=0, we will get 'x_van4'
	mode=1, we will get ('x', 'van4')
	mode=2, we will get 'x_van_4' 
	mode=3, we will get ('x', 'van', '4')"""
	assert syllable[-1].isdigit()
	consonants=['ch','sh','zh','b','p','m','f','d','t','n','l','g','k','h','j','q','x','y','w','r','z','c','s']
	cut=0
	if len(syllable)>=3:
		if syllable[0:2] in consonants:
			cut=2
		elif syllable[0] in consonants:
			cut=1
	assert mode in range(0,4)
	if mode==0:
		return syllable[0:cut]+'_'+syllable[cut:]
	elif mode==1:
		return syllable[0:cut],syllable[cut:]
	elif mode==2:
		return syllable[0:cut]+'_'+syllable[cut:-1]+'_'+syllable[-1]
	elif mode==3:
		return syllable[0:cut],syllable[cut:-1],syllable[-1]
