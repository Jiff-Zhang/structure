# -*- coding: utf-8 -*- 
import os
import re
import sys

consonants=['ch','sh','zh','b','p','m','f','d','t','n','l','g','k','h','j','q','x','y','w','r','z','c','s']

def take_apart(phone):
	consonant=None
	vowel=None
	tone=phone[-1]
	for con in consonants:
		if phone.startswith(con):
			consonant=con
			break
	
	if consonant is None:
		length=0
	else:
		length=len(consonant)
	
	vowel=phone[length:len(phone)-1]
	return consonant,vowel,tone
	

#定义
#未知的音素
unknown='uk'

#路径
#working_dir=os.getcwd()
working_dir=os.path.split(sys.argv[0])[0]
prosodylabeling='prosodylabeling/KING_tts001中文单句_100001-101000.txt'
sfs='sfs1/tts001'
#print os.listdir(working_dir+sfs)

dir_sfs=os.path.join(working_dir,sfs)
dir_pro=os.path.join(working_dir,prosodylabeling)
assert os.path.exists(dir_sfs)
assert os.path.exists(dir_pro)   
#print dir_sfs

#尝试第一个文件
pro_file=open(dir_pro)
for front in range(1,2):
	pro1=pro_file.readline()
	pro2=pro_file.readline()
	#取出文字和拼音
	word=pro1.split('\t')[1]
	word=word.strip()
	spell=pro2.split('\t')[1]
	spell=spell.strip()
	#print word,spell

	#分离出文字集、韵律以及拼音
	words=re.split('#\d',word)
	rhythms=re.findall('\d',word)
	syllables=spell.split()
	#print words,syllables,rhythms
	num_for_rhythm=[len(x)/3 for x in words]
	num_for_rhythm_1=[sum(num_for_rhythm[0:x]) for x in range(1,len(num_for_rhythm)+1)]
	num_for_rhythm_2=[sum(num_for_rhythm[0:x]) for x in [i+1 for i,v in enumerate(rhythms) if v>='2']]+[num_for_rhythm_1[-1]]
	num_for_rhythm_3=[sum(num_for_rhythm[0:x]) for x in [i+1 for i,v in enumerate(rhythms) if v>='3']]+[num_for_rhythm_1[-1]]
	num_for_rhythm_4=[sum(num_for_rhythm[0:x]) for x in [i+1 for i,v in enumerate(rhythms) if v>='4']]+[num_for_rhythm_1[-1]]

	print rhythms,num_for_rhythm,num_for_rhythm_1,num_for_rhythm_2,num_for_rhythm_3,num_for_rhythm_4
	#index=[x>10 for x in num_for_rhythm_1].index(True)
	#print index
	#print map(int,rhythms)
	#print map(int,rhythms).index(4)
	syllables_phones=map(take_apart,syllables)

	#时间文件，分离出时间[0]和状态[1]
	sfs_file='%d.SFS1' % (100000+front)
	assert os.path.exists(os.path.join(dir_sfs,sfs_file))
	file_sfs=open(os.path.join(dir_sfs,sfs_file))
	sfs=file_sfs.read()
	times_states=sfs.split()
	#sfs=file_sfs.readline()
	#times_states=[]
	#while sfs:
		#sfs_split=sfs.strip().split(' ')
		#times_states.append(sfs_split)
		#sfs=file_sfs.readline()
	#print times_states	
	
	times=times_states[0::2]
	states=times_states[1::2]
	#print times,states

	#初始化p
	p1=p2=p3=p4=p5=unknown
	p6=p7='0'

	syllable_order_p=0
	phone_type=0

	if states[0]=='s':
		p4='sil'
	elif states[0]=='d':
		p4='brk'
	else:
		while syllables_phones[syllable_order_p][phone_type] is None:
			phone_type+=1
			syllable_order_p+=phone_type/2
			pnone_type=phone_type%2
		p4=syllables_phones[syllable_order_p][phone_type]
		phone_type+=1
		syllable_order_p+=phone_type/2
		phone_type=phone_type%2
	
	if states[1]=='s':
		p5='sil'
	elif states[1]=='d':
		p5='brk'
	else:
		while syllables_phones[syllable_order_p][phone_type] is None:
			phone_type+=1
			syllable_order_p+=phone_type/2
			phone_type=phone_type%2
		p5=syllables_phones[syllable_order_p][phone_type]
		phone_type+=1
		syllable_order_p+=phone_type/2
		phone_type=phone_type%2

	
	#初始化abc
	a1=a2=b1=b2=c1=c2=unknown
	a3=b3=c3=unknown
	a4=b4=c4='0'
	b5=b6=b7=b8=b9=b10=b11=b12='0'

	syllable_order_c=0
	c1=unknown if syllables_phones[syllable_order_c][0] is None else syllables_phones[syllable_order_c][0]
	c2=unknown if syllables_phones[syllable_order_c][1] is None else syllables_phones[syllable_order_c][1]
	c3=syllables_phones[syllable_order_c][2]
	c4='1' if syllables_phones[syllable_order_c][0] is None else '2'
	syllable_order_c+=1

	for i in range(len(states)-1):
		outstr=times[i]+'\t'+times[i+1]+'\t'
		
		#p
		p1=p2
		p2=p3
		p3=p4
		p4=p5
		
		if i+2>len(states)-1:
			p5=unknown
		elif states[i+2]=='s':
			p5='sil'
		elif states[i+2]=='d':
			p5='brk'
		else:
			while syllables_phones[syllable_order_p][phone_type] is None:
				phone_type+=1
				syllable_order_p+=phone_type/2
				phone_type=phone_type%2
			p5=syllables_phones[syllable_order_p][phone_type]
			phone_type+=1
			syllable_order_p+=phone_type/2
			phone_type=phone_type%2
	
		if p3=='sil' or p3=='brk':
			p6=p7='0'
		elif p3 in consonants:
			p6='1'
			p7='2'
		elif p2 in consonants:
			p6='2'
			p7='1'
		else:
			p6='1'
			p7='1'

		outstr+=p1+'\t'+p2+'\t'+p3+'\t'+p4+'\t'+p5+'\t'+p6+'\t'+p7+'\t'
		
		#abc
		a1=b1
		a2=b2
		a3=b3
		a4=b4
		if p3=='sil' or p3=='brk':
			b1=b2=b3=unknown
			b4=b5=b6=b7=b8=b9=b10=b11=b12='0'
		elif not p2 in consonants:
			b1=c1
			b2=c2
			b3=c3
			b4=c4

			index=[x>=syllable_order_c for x in num_for_rhythm_1].index(True)
			if index==0:
				b5=str(syllable_order_c)
			else:
				b5=str(syllable_order_c-num_for_rhythm_1[index-1])
			b6=str(num_for_rhythm_1[index]+1-syllable_order_c)
			
			index=[x>=syllable_order_c for x in num_for_rhythm_2].index(True)
			if index==0:
				b7=str(syllable_order_c)
			else:
				b7=str(syllable_order_c-num_for_rhythm_2[index-1])
			b8=str(num_for_rhythm_2[index]+1-syllable_order_c)
			
			index=[x>=syllable_order_c for x in num_for_rhythm_3].index(True)
			if index==0:
				b9=str(syllable_order_c)
			else:
				b9=str(syllable_order_c-num_for_rhythm_3[index-1])
			b10=str(num_for_rhythm_3[index]+1-syllable_order_c)
			
			index=[x>=syllable_order_c for x in num_for_rhythm_4].index(True)
			if index==0:
				b11=str(syllable_order_c)
			else:
				b11=str(syllable_order_c-num_for_rhythm_4[index-1])
			b12=str(num_for_rhythm_4[index]+1-syllable_order_c)

			if syllable_order_c<len(syllables_phones):
				c1=unknown if syllables_phones[syllable_order_c][0] is None else syllables_phones[syllable_order_c][0]
				c2=unknown if syllables_phones[syllable_order_c][1] is None else syllables_phones[syllable_order_c][1]
				c3=syllables_phones[syllable_order_c][2]
				c4='1' if syllables_phones[syllable_order_c][0] is None else '2'
				syllable_order_c+=1
			else:
				c1=c2=c3=unknown
				c4='0'
		
		outstr+=a1+'\t'+a2+'\t'+a3+'\t'+a4+'\t'+b1+'\t'+b2+'\t'+b3+'\t'+b4+'\t'+b5+'\t'+b6+'\t'+b7+'\t'+b8+'\t'+b9+'\t'+b10+'\t'+b11+'\t'+b12+'\t'+c1+'\t'+c2+'\t'+c3+'\t'+c4+'\t'

		#print syllable_order_c
		print outstr
			
	
	file_sfs.close()

pro_file.close()
