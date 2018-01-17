# -- encoding:utf-8 --
from sentence import Sentence
from word import Word
from os.path import exists
import re
from sys import argv

## 存放文本（包含文本、韵律和拼音）
txt_file='/home/willing/Documents/King-TTS-003/data/prosodylabeling/KING_tts001中文单句_100001-101000.txt'
# seg_file='/home/willing/proj/frontend/king-tts-words/tts001.txt'
## 词性文本（包含文本和词性）
pos_file='/home/willing/proj/frontend/king-tts-pos/tts001.txt'

if len(argv)==3:
	script,txt_file,pos_file=argv
else:
	assert len(argv)==1

assert exists(txt_file)
# assert exists(seg_file)
assert exists(pos_file)

txt_file=open(txt_file)
## 读入文本韵律行
txt_line=txt_file.readline()
# seg_file=open(seg_file)
# seg_line=seg_file.readline()
# seg_line=seg_line[4:]
pos_file=open(pos_file)
## 读入词性行
pos_line=pos_file.readline()
## 由于词性文本第一行前会有一段无效信息，所以先去除，具体原因暂不清楚
pos_line=pos_line[6:]

while txt_line:
	# print sent
	
	## 读入音节行
	syl_line=txt_file.readline()
	
	## 去除文本韵律行、词性行以及音节行前后的无用空白（制表符、换行等）
	txt_line=txt_line.strip()
	syl_line=syl_line.strip()
	# seg_line=seg_line.strip()
	pos_line=pos_line.strip()
	
	## 分离文本韵律行的行号
	sent_id,sent=txt_line.split('\t')

	# print sent_id,' ',
	
	# print ' '.join(re.split('#[1-4]',sent))
	# print ' '.join(re.findall('#[1-4]',sent))
	
	## 提取文本txt_words和韵律rhythm
	txt_words=re.split('#[1-4]',sent)
	rhythm=re.findall('#[1-4]',sent)
	rhythm.append('#4')
	assert len(rhythm)==len(txt_words)
	# seg_words=re.split('\t',seg_line)
	## 切分词性行
	pos_words=re.split('\t',pos_line)
	# print len(seg_words),len(pos_words)
	# assert len(seg_words)==len(pos_words)

	# print ' '.join(txt_words)
	# print ' '.join(seg_words)
	# print map(len,seg_words)
	
	## 将所需信息存储进Sentence对象
	sentence=Sentence()
	start=0
	total_bit=0
	for pos_word in pos_words:
		txt,pos=pos_word.split('_')
		pre_set_rhythm='#0'
		while start<len(txt_words):
			total_bit+=len(txt_words[start])
			if total_bit>len(txt):
				total_bit-=len(txt)+len(txt_words[start])
				break
			elif total_bit==len(txt):
				total_bit=0
				pre_set_rhythm=rhythm[start]
				start+=1
				break
			pre_set_rhythm=max(pre_set_rhythm,rhythm[start])
			start+=1

		sentence.append(txt,pos,pre_set_rhythm)

	print sent_id,'\t',sent
	# print len(rhythm),rhythm[len(rhythm)-1]
	# print pos_line
	print '\t',
	sentence.show()
	# print sentence.length()
	print '\t',syl_line
	print

	## 读入下一行 
	txt_line=txt_file.readline()
	# seg_line=seg_file.readline()
	pos_line=pos_file.readline()

txt_file.close()
# seg_file.close()
pos_file.close()
