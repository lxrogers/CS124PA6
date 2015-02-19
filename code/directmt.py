import sys
import os
import collections
import math
import time

class Translator:

    def __init__(self):
    	pass;

    def readDictionary(self, filename):
    	pass;

    def readJoinFiles(self, file1, file2):
    	return zip(readFile(file1).split("\n"), readFile(file2).split("\n"));

    # Read in StatMT data and then train the differences between english and french among translations
    def trainStructuralClassifier(self):
    	pass;

    def trainLM(self):
    	pass;

    def trainMA(self):
    	pass;

    def translate(self):
    	pass; #reorder sentence, validate









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

     
def runTranslations(v):
	if(v): print "Starting up the Translator...";
	t = Translator();
	t.trainStructuralClassifier();


def main():
	start = time.time();
	shouldTime = False;
	verbose = False;

	for i in sys.argv[1:]:
		shouldTime = shouldTime || i == "-t";
		verbose = verbose || i == "-v";
			
	runTranslations(verbose);

	if(shouldTime): print '\033[92m' + "\nFinished in ", int(time.time() - start)/100/10.0, "seconds!\n" + '\033[0m';
	sys.exit();

# Boilerplate
if __name__ == "__main__":
        main();