### Instructions

Use que_without_stopwords.py file to generate a json file (i.e que.json) that would contain questions without any stopwords. This json file is fed into SEMPRE to generate the output. 
Use earl.py file to generate the lexicon files. This script first calls the live demo api of earl to produce a text file (i.e earl_api_output) and uses it to produce output.lexicon. Then it further creates a dbpedia.lexicon file to which contains lexemes as accepted by the SEMPRE framework. The main difference between output.lexicon and dbpedia.lexicon is that the latter is free of any special characters such as- ',!,@,# etc.
We can also set the number of candidates we want for a lexeme in the earl.py file.
Use output.py to generate the csv file containing questions, their logical formula and sparql query. We can set how many candidates we want for a particular question.
Command for producing output in SEMPRE is-
./run @mode=simple-freebase-nocache @sparqlserver=localhost:3001 -Grammar.inPaths dbpedia/dbpedia.grammar -SimpleLexicon.inPaths dbpedia/dbpedia.lexicon -FeatureExtractor.featureDomains rule opCount constant whType span lemmaAndBinaries denotation lexAlign joinPos skipPos -Dataset.inPaths test:dbpedia/que.json -Learner.maxTrainIters 0 -SparqlExecutor.verbose 10 -exec.execDir dbpedia/out/
