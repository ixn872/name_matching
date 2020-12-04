import Levenshtein
from Levenshtein import distance
import pandas as pd
import difflib
from difflib import SequenceMatcher as m
import re

data = pd.read_csv('name_mismatches.csv',names=['v1','v2'])

print(data.head(10))

thres=0.72
L1=data['v1']
L2=data['v2']
Temp=[]
similarities=[]
def is_female_equivalent(a,b):
	pattern1 = re.compile('(.{2}$)')
	pattern2 = re.compile('(.{1}$)')
	for i in [a,b]:
		if SeqM>thres and re.search(pattern2,a).group(1)=='a' and re.search(pattern1,b).group(1) in ['os','as'] :
			return 1
		elif SeqM>thres and re.search(pattern2,b).group(1)=='a' and re.search(pattern1,a).group(1) in ['os','as']:
			return 1
	return 0
              

for i in zip(L1,L2):
	
	a=i[0]
	b=i[1]
	Levenshtein=distance(a,b)
	custom_metric = Levenshtein/(len(a+b))
	SeqM = m(None,a,b).ratio()
	print("Levenshtein distance:",Levenshtein)
	print("Custom metric:",custom_metric)
	print("Sequence matcher:",SeqM)
	if SeqM>thres and is_female_equivalent(a,b)==0:
		Temp.append(1)
		similarities.append(SeqM)
		continue
	elif SeqM>thres and is_female_equivalent(a,b)==1:
		similarities.append(SeqM)
		Temp.append(0)
		continue
	elif SeqM<=thres:
		similarities.append(SeqM)
		Temp.append(0)
		continue
			
#print(Temp)

#print(Levenshtein.distance('nikol','nicole'))
#x=Levenshtein.distance('nikol','nicole')
#metric = float(x)/(len('nikol')+len('nicole')) #you want this close to 0
#print(metric)

data["isMatch"]=Temp
data["similarities"]=similarities
print(data)


data.to_csv('./name_match_results.csv')
