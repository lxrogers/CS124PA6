import sys
import getopt
import os
import collections
import math
import time

class StatisticalMT:

    def __init__(self):
    	pass;

    # Takes in two files and returns a list of tuples that are corresponding translated sentences
    def readTrainingData(self, file1, file2):
    	return zip(readFile(file1).split("\n"), readFile(file2).split("\n"));


    def train(self, englishfilename, frenchfilename):
    	translations = self.readTrainingData(englishfilename, frenchfilename);
    	pass;


    def translate(self, infile, outfile):
    	# TODO: translate infile and write translations to outfile
    	pass;


    def validate(self, actualfile, translatedfile):
		command = "python bleu_score.py " + actualfile + " " + translatedfile;
		os.system(command); 









##############################################################################################################################
##############################################################################################################################
#################################################### UTILITY FUNCTIONS #######################################################
##############################################################################################################################
##############################################################################################################################

# Reads a file and returns the text contents
def readFile(filename):
	with open(filename) as f: return f.read();

# Throws an error.
# 		First param: String that contains error/notification
# 		Second param: Whether to halt program execution or not.
def throwError(message, shouldExit):
	print '\033[93m' + str(message) + '\033[0m';
	if(shouldExit): sys.exit();







##############################################################################################################################
##############################################################################################################################
################################################# SYSTEM CALL FUNCTIONS ######################################################
##############################################################################################################################
##############################################################################################################################

# command line reference to train, generate and validate the translations of our statistical MT model
# 
# Example call: python statmt.py all
#     
def all():
	output1 = "../data/translations/newstest2012-translation.en";
	output2 = "../data/translations/newstest2013-translation.en";

	mt = StatisticalMT();
	mt.train("../data/train/europarl-v7.fr-en.en", "../data/train/europarl-v7.fr-en.fr");

	mt.translate('../data/dev/newstest2012.fr', output1);
	mt.translate('../data/test/newstest2013.fr', output2);

	mt.validate('../data/dev/newstest2012.en', output1);
	mt.validate('../data/test/newstest2013.en', output2);


# command line reference to generate and output new translations.
# 
# Example call: python statmt.py generateTranslations
#     
def generateTranslations():
	output1 = "../data/translations/newstest2012-translation.en";
	output2 = "../data/translations/newstest2013-translation.en";

	mt = StatisticalMT();
	mt.train("../data/train/europarl-v7.fr-en.en", "../data/train/europarl-v7.fr-en.fr");

	mt.translate('../data/dev/newstest2012.fr', output1);
	mt.translate('../data/test/newstest2013.fr', output2);
  

# command line reference to test the current outputed translations.
# 
# Example call: python statmt.py testTranslations
#       
def testTranslations():
	mt = StatisticalMT();
	output1 = "../data/translations/newstest2012-translation.en";
	output2 = "../data/translations/newstest2013-translation.en";

	mt.validate('../data/dev/newstest2012.en', output1);
	mt.validate('../data/test/newstest2013.en', output2);


# command line reference, calls whatever functions you pass as parameter
# 
# Example call: python statmt.py all
# 						which is the equivalent to:
# 				python statmt.py generateTranslations testTranslations
# 				
# Additionally, you can call with a -t flag to record the time of the program execution
# 
# Example call: python statmt.py all -t
# 						which is equivalent to:
# 				python statmt.py -t all
def main():
	start = time.time();
	shouldTime = False;

	for question in sys.argv[1:]:

		if(question == "-t"): shouldTime = True;
		else: eval(question.lower() + "()");

	if(shouldTime): print '\033[92m' + "\nFinished in ", int(time.time() - start)/100/10.0, "seconds!\n" + '\033[0m';
	sys.exit();

# Boilerplate
if __name__ == "__main__":
        main();