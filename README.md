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
	2) Pipeline - Cayman add Print Report/debug
				- Lawrence add 4/5/6 strategy translations


I. STRUCTURAL TRANSLATION

	1) Convert all test sentences to POS (part of sentence) - Raissa
		a) Using POS Classifier 
			-Train on outside dataset
			-Does NLTK POS Classifier work (I think there's one for French)

	2) Find order/matching of sentence by weights of:
		a) Handwritten rules - Cayman
			-Switch indirect objects with prepositions and objects and put after verb (#1)
			-Switch direct objects and put after verbs (#2)
			-Switch adjectives and noun placements (#3)
		b) Structural  (#4) (French Structure -> English Structure); - Raissa
			-Train on POS Classified statmt/POS data


II. PHRASE TRANSLATION

	3) Phrase Detection/Translation (#4) - Cayman
		-Not sure how I'm going to do this


III. WORD TRANSLATION

	4) Naive Bayes to pick translation (#6) - Andrew
		-Train on words in sentences, POS, stemming and Stupid Backoff 
		-Train on statmt data, pick highest probability words we've seen


IV. WRITEUP - Lawrence


COMMAND LINE REFERENCE
===========================================================================

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