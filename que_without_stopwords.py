import pandas as pd
import json
import spacy
spacy_nlp = spacy.load('en_core_web_sm')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
customize_stop_words = ['which','give','where','in','what','who','name','list','why','did','is','are','was','were','the','show','do','does','tell','s']
for w in customize_stop_words:
    spacy_nlp.vocab[w].is_stop = True
customize_stop_words = ['of','not','and','part','that','name','list']

for w in customize_stop_words:
    spacy_nlp.vocab[w].is_stop = False

f= open("./que.json", "w")
f1= open("./que.txt","w")
f.write("[")
data= pd.read_csv("./kr2ml_train.tsv",sep='\t', header=None)
flag=0
for i in range(data.values.shape[0]):
	que= data.values[i][0]
	que= que[0].lower() + que[1:] 
	que=que.replace("'","").replace('"', '')
	if que.split()[0]=='how' and que.split()[1]=='many':
		flag=1 
	doc = spacy_nlp(que)
	tokens = [token.text for token in doc if not token.is_stop]
	text= (" ").join(tokens)
	if flag==1:
		text='how many '+text
		flag=0
	text=text.strip()
	dic={}
	dic["utterance"]=text
	json_object = json.dumps(dic)
	f.write(json_object) 
	f.write(",\n")
	f1.write(text)
	f1.write("\n")
f.write("]")