# CS124PA6
CS124 Machine Translation Assignment

By Cayman Simpson, Lawrence Rogers, Andrew Mather, and Raissa Largman

This is an implementation of Direct Machine Translation. We are implementing the following improvements:

Dependencies:
NLTK
	-Documentation: http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
	-Installation: : sudo easy_install pip / sudo pip install -U numpy / sudo pip install -U nltk

0. PRE-STUFF
	1) Create Dictionary/Testing - Raissa
	2) Human Translations - Cayman/Raissa
	3) Pipeline - Cayman add Print Report/debug
				- Lawrence add 4/5/6 strategy translations


I. STRUCTURAL TRANSLATION

	1) Convert all test sentences to POS (part of sentence) - Raissa
		a) Using POS Classifier 
			-Train on outside dataset

	2) Find order/matching of sentence by weights of:
		a) Handwritten rules (#1) - Cayman
		b) Structural  (#2) (French Structure -> English Structure); - Raissa
			-Train on POS Classified statmt/POS data


II. PHRASE TRANSLATION

	3) Phrase Detection/Translation (#3) - Cayman
		-Not sure how I'm going to do this


III. WORD TRANSLATION - WEIGHTED CHOICE

	4) Naive Bayes to pick translation (#4) - Andrew
		-Train on words in sentences, POS, stemming (#5) and Stupid Backoff 
		-Train on statmt data, pick highest probability words we've seen
	5)  



To train, test and validate this model, use:

	python directmt.py all

The above command line will call all strategies, 0 - 6 and output them to the appropriate folder. If you want to test a certain level of translation, use:

	python directmt.py 0

This is also extendable if you want to do the first three levels of translation:

	python directmt.py 0 1 2 3

It can also be called with an optional '-t' flag that will time the program execution:

	python directmt.py 0 1 2 -t


To see the impact of all our methodologies on the translations, call the script with a verbose flat '-v':

	python directmt.py -v (-t) 0 1 2

	or equivalently:

	python directmt.py 0 1 2 (-t -v)


For more details on the command line reference, observe the bottom of statmt.py for details on how the terminal calling interacts with the building and validating of the direct translation model itself.