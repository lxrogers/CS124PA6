# CS124PA6
CS124 Machine Translation Assignment

By Cayman Simpson, Lawrence Rogers and Andrew Mather

Implementing the Statistical Machine Translation
Base algorithm on page 13: https://spark-public.s3.amazonaws.com/cs124/slides/mt2.pdf

To train, test and validate this model, use:

	python statmt.py all


It can also be called with an optional '-t' flag that will time the program execution:

	python statmt.py all -t


To train and just generate translations, use:

	python statmt.py generateTranslations (-t)


To validate current translations, use:
	
	python statmt.py testTranslations (-t)


For more details on the command line reference, observe the bottom of statmt.py for details on how
the terminal callin interacts with the building and validating of the statistical model itself.