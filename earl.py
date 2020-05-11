import json
import os
from textrazor import *
import re
# data= pd.read_csv("./kr2ml_train.tsv",sep='\t', header=None)
# client = TextRazor('a02e9cce51c6c087f150269a4eab62812057696716b70eb1f2e0a8fd', extractors=["entities","phrases"])
# for i in range(data.values.shape[0]):
# 	que= data.values[i][0]
# 	# print(que.replace("'", ""))
# 	if i==0:
# 		text="curl -XPOST \'https://earldemo.sda.tech/earl/api/processQuery\' -H \'Content-Type:application/json\' -d\' {\"nlquery\":\""+que.replace("'", "")+"\", \"pagerankflag\": false}\' > ./earl_api_output.txt"
# 	else:
# 		text="curl -XPOST \'https://earldemo.sda.tech/earl/api/processQuery\' -H \'Content-Type:application/json\' -d\' {\"nlquery\":\""+que.replace("'", "")+"\", \"pagerankflag\": false}\' >> ./earl_api_output.txt"
# 	os.system(text)
# 	os.system('echo "" >> ./earl_api_output.txt')
# 	print(i)

file1 = open("./output.lexicon","w")
# f1 = open("./que.txt")
results = []
with open('earl_api_output.txt') as f:
	for jsonObj in f:
		try:
			resultDict = json.loads(jsonObj)
			results.append(resultDict)
		except:
			print("Error",i)
f.close()

np=[]
lexeme_count={}
for result in results:
	type=result["ertypes"]
	for i,j in enumerate(result["chunktext"]):
		dict_={}
		for l in result["rerankedlists"][str(i)]:
			dict_["lexeme"]=j["chunk"]
			try:
				if l[1].split('/')[-2]=="property":
					 dict_["formula"]= "fb:prop.prop."+l[1].split('/')[-1]
				elif l[1].split('/')[-2]=="ontology":
					if l[1].split('/')[-1][0].isupper():
						dict_["formula"]= "(fb:rdf.type.prop fb:nounphrase."+l[1].split('/')[-1]+")"
					else:
						dict_["formula"]= "fb:phrase.prop."+l[1].split('/')[-1]
				else:
					dict_["formula"]= "fb:phrase."+l[1].split('/')[-1]
				if j["chunk"] not in lexeme_count.keys():
					lexeme_count[j["chunk"]]=0
				if lexeme_count[j["chunk"]]<3: # set number of candidates here
					lexeme_count[j["chunk"]]+=1
					file1.write(json.dumps(dict_))
					file1.write("\n")
			except:
				print(j["chunk"])
				pass

f1= open('dbpedia.lexicon','w')
with open('output.lexicon') as f:
	for jsonObj in f:
		resultDict = json.loads(jsonObj)
		l=resultDict['formula']
		if l[:15]=='fb:phrase.prop.':
			l=l[:15]+re.sub('[!,-.~`%^*+=?/<>";:&@#$()\']', '', l[15:])
		elif l[:4]=='(fb:':
			l="(fb:rdf.type.prop fb:nounphrase."+re.sub('[!,-.~`%^*+=?/<>";:&@#$()\']', '', l[32:][:-1])+")"
		elif l[:13]=='fb:prop.prop.':
			l=l[:13]+re.sub('[!,-.~`%^*+=?/<>";:&@#$()\']', '', l[13:])
		else:
			l=l[:10]+re.sub('[!,-.~`%^*+=?/<>";:&@#$()\']', '', l[10:])
		resultDict['formula']=l
		f1.write(json.dumps(resultDict))
		f1.write("\n")