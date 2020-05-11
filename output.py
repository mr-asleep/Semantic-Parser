import re
import pandas as pd
from difflib import get_close_matches
import json

form=[]
with open('output.lexicon') as f:
    for jsonObj in f:
        resultDict = json.loads(jsonObj)
        form.append(resultDict['formula'])

lines=[]
with open ('../dbpedia/out/log', 'rt') as myfile: 
    for myline in myfile:
        lines.append(myline.strip())

data= pd.read_csv("./kr2ml_train.tsv",sep='\t', header=None)

c_lf=0
c_sq=0
dic={}
temp=""
key=""
flag=0
formula=[]
sparql=[]
ind=0
k=-1
for  i,l in enumerate(lines):
	try:
		if l[:8]=='Example:':
			key= l[8:][:-1].strip()
			if flag==1:
				if c_sq != c_lf:
					c_sq=min(c_lf,c_sq)
					c_lf=c_sq
				if c_lf!=0:
					ind+=1
					dic[str(ind)+'. '+data.values[k][0]]={'logical formula':formula[:c_lf],'sparql query':sparql[:c_sq]} 
			temp=key
			flag=1
			c_lf=0
			c_sq=0
			formula=[]
			sparql=[]
			k+=1
		if l[:5]=='Pred@':
			result=re.search('formula(.+?)value', l)
			formula.append(result.group(1)[:-3].strip())
			c_lf+=1
		if l.find('SparqlExecutor.execute: PREFIX')!=-1:
			result=re.search('<http://rdf.freebase.com/ns/>(.*)LIMIT 10', l)
			if result.group(1) not in sparql:
				sparql.append(result.group(1).strip())
				c_sq+=1
	except:
		pass
if c_sq != c_lf:
	c_sq=min(c_lf,c_sq)
	c_lf=c_sq
if c_lf!=0:	
	ind+=1
	dic[str(ind)+'. '+data.values[k][0]]={'logical formula':formula[:c_lf],'sparql query':sparql[:c_sq]}
for key in dic.keys():
	length=min(3,len(dic[key]['logical formula']))                  # select the number of candidates here
	dic[key]['logical formula']=dic[key]['logical formula'][:length]
	dic[key]['sparql query']=dic[key]['sparql query'][:length]

utterance=[]
sparql=[]
formula=[]
for key in dic.keys():
	for l in dic[key]['logical formula']:
		formula.append(l)
		utterance.append(key)
	for l in dic[key]['sparql query']:
		sparql.append(l)

for i,s in enumerate(sparql):
	l=re.split(r'([{}()\s=])', s)
	# print(l)
	for j,f in enumerate(l):
		try:
			if f[:4]=='fb:p' or f[:4]=='fb:n':
				l[j]=get_close_matches(f,form,n=1)[0]
				if l[j][:15]=='fb:phrase.prop.':
					l[j]='dbo:'+l[j][15:]
				elif l[j][:14]=='fb:nounphrase.':
					l[j]='dbo:'+l[j][14:].capitalize() 
				elif l[j][:13]=='fb:prop.prop.':
					l[j]='dbp:'+l[j][13:]
				else:
					l[j]='dbr:'+l[j][10:]
			if f[:4]=='fb:r':
				l[j]='rdf:type'
		except:
			pass
	sparql[i]=("").join(l)
	print(i)

dict = {'Question' : utterance, 'Logical Formula' : formula,'Sparql Query':sparql}
df = pd.DataFrame(dict)
df.to_csv('./out.csv', index=False)