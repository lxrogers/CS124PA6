# CS124PA6
CS124 Machine Translation Assignment

By Cayman Simpson, Lawrence Rogers and Andrew Mather

This is an implementation of Direct Machine Translation. We are implementing the following improvements:

Dependencies:
NLTK
	-Documentation: http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
	-Installation: : sudo easy_install pip / sudo pip install -U numpy / sudo pip install -U nltk

I. STRUCTURAL TRANSLATION

	1) Convert all test sentences to POS (part of sentence)
		a) Using POS Classifier
			-Train on outside dataset

	2) Find order/matching of sentence by weights of:
		a) Handwritten rules (#1)
		b) Structural  (#2)
			-Train on POS Classified statmt data


II. PHRASE TRANSLATION

	3) Phrase Detection/Translation (#3)
		-Needs to be done before anything else

III. WORD TRANSLATION - WEIGHTED CHOICE

	4) Language Models (Stupid Backoff?) (#4)
		-Train on statmt data, pick highest probability words we've seen
	5) Naive Bayes to pick translation (#5)
		-Train on words in sentences and POS
	6) ???

	

To train, test and validate this model, use:

	python directmt.py


It can also be called with an optional '-t' flag that will time the program execution:

	python directmt.py -t


To see the impact of all our methodologies on the translations, call the script with a verbose flat '-v':

	python directmt.py -v (-t)


For more details on the command line reference, observe the bottom of statmt.py for details on how
the terminal callin interacts with the building and validating of the statistical model itself.