#! /usr/local/bin/python
# Andrew Mather, Cayman Simpson, Lawrence Rogers, Raissa Largman
# CS124, Created: 17 February 2015
# file: directmt.py

# The purpose of this file is to use direct machine translation
# to translate a small corpus of sentences using techniques
# learned in CS124.

import sys
import os
from os import listdir
from os.path import isfile, join
import collections
import math
import time
import random
from nltk.stem.snowball import FrenchStemmer
from nltk.tag.stanford import POSTagger
from PhraseTranslator import PhraseTranslator
from NaiveBayes import NaiveBayes

# stemmer = FrenchStemmer
# stemmer.stem('voudrais')

class Translator:

    def __init__(self):
      self.dicFilename = "";
      self.dictionary = self.readDictionary(self.dicFilename);

      self.trainFilename = "";

      self.devFrenchFilename = "";
      self.devEnglishFilename = "";

      self.testFrenchFilename = "";
      self.testEnglishFilename = "";

      self.targetSentences = [];

      self.POSClassifier = POSTagger(
        'stanford-postagger/models/french.tagger', 
        'stanford-postagger/stanford-postagger.jar', 
        'utf8'
      )
      self.EnglishPOSClassifier = POSTagger(
        'stanford-postagger/models/english-bidirectional-distsim.tagger', 
        'stanford-postagger/stanford-postagger.jar', 
        'utf8'
      )
      self.structuralClassifier = NaiveBayes();
      self.phraseTranslator = None;

    def readDictionary(self, filename):
      dic = {};
      with open(filename) as f:
        for line in f:
          dic[line.split("\t")[0]] = line.split("\t")[1].split(",");


    def readJoinFiles(self, file1, file2):
      return zip(readFile(file1).split("\n"), readFile(file2).split("\n"));

    # Read in StatMT data and then train the differences between english and french among translations
    FRENCH_PARLIAMENT_FILEPATH = '../data/parliament_french.txt'
    ENGLISH_PARLIAMENT_FILEPATH = '../data/parliament_english.txt'
    def trainStructuralClassifier(self):
      frenchPOSTrainData = self.POSClassifier.tag_sents(
        readFile(FRENCH_PARLIAMENT_FILEPATH).split("\n")
      )
      englishPOSTrainData = self.EnglishPOSClassifier.tag_sents(
        readFile(ENGLISH_PARLIAMENT_FILEPATH).split("\n")
      )
      self.structuralClassifier.addExamples(frenchPOSTrainData, englishPOSTrainData)


    def trainLanguageModel(self):
      pass;

    def translate(self):
      pass; #reorder sentence, validate

    def reorderTargets(self, sentences, weighted):
      pass; #weighted would have classifier

    def initializePhraseTranslator():
      if(self.phraseTranslator != None): self.phraseTranslator = PhraseTranslator(self.dictionary, self.POSClassifier);

    # Raissa - Basically, I'll use a specialized Language Model to find phrases and mark them
    # with tags so that you know how to treat them when Reordering sentences based on parts of speech
    # 
    # Examples:
    # Il y a un chien => <NOUN,VERB>Il y a<NOUN,VERB> un chien =(eventually)=> There is un chien
    # La voiture est tombee en panne => La voiture est <VERB,ADJECTIVE>tombee en panne<VERB,ADJECTIVE>
    # Qu'est-ce que c'est? => <DIRECT OBJECT>Qu'est-ce que<DIRECT OBJECT> c'est?
    # 
    # I'll keep my tags consistent with the POS tags in the .pos files
    def markPhrases(self, sentences):
      if(isinstance(sentences[0], tuple)):
        english = map(lambda x: x[1], sentences);
        french = self.phraseTranslator.markPhrases(map(lambda x: x[0], sentences));
        return zip(french, english);
      else: return self.phraseTranslator.markPhrases(sentences);

    # Returns true if I marked a phrase, in the format mentioned above
    #   (checks for the <> tag)
    def markedPhrase(self, token):
      return self.phraseTranslator.isMarkedPhrase(token);

    # Converts a french phrase into an english one.
    def translatePhrase(self, token):
      return self.phraseTranslator.translatePhrase(token);




##############################################################################################################################
##############################################################################################################################
#################################################### UTILITY FUNCTIONS #######################################################
##############################################################################################################################
##############################################################################################################################

# Reads a file and returns the text contents
def readFile(filename):
  with open(filename) as f: return f.read();

# Throws an error.
#     First param: String that contains error/notification
#     Second param: Whether to halt program execution or not.
def throwError(message, shouldExit):
  print '\033[93m' + str(message) + '\033[0m\n';
  if(shouldExit): sys.exit();

# Outputs a zipped array to a file
#     First param: Joined Array to output
#     Second param: filename
def outputJoin(joined, filename):
  try:
    w = open(filename, 'w');
    for tup in joined:
      w.write(tup[0] + "\n" + tup[1] + "\n\n");
    w.close();  
  except IOError:
    print "Could not write translation to '" + filename + "'."; 

#print report of sentences
def printReport(dev):
  pass;

def getRecursivePosFiles(path):
  paths = [path];
  files = [];
  while(len(paths) > 0):
    children = [f for f in listdir(paths[0])];
    for child in children:
       if not isfile(join(path,f)) and "." not in f: # not invisible and a directory
        paths.append(child);

       if isfile(join(path,f)) and ".pos" in f:
        files.append(child);

    paths = paths[1:]; #remove teh path we just looked at

  return files;

##############################################################################################################################
##############################################################################################################################
################################################# SYSTEM CALL FUNCTIONS ######################################################
##############################################################################################################################
##############################################################################################################################

t = None;

def zeroStrategyTranslations(v):
  if(v): print "\nStarting up the Translator for stage 0...";
  if(v): print "Random Direct Machine Translation...";
  t = Translator();
  t.readDictionary();

  if(v): print "Translating Sentences...";

  dev = readJoinFile(t.devFrenchFilename, t.devEnglishFilename);
  translations = [];
  for french, english in dev:
    translations.append(map(lambda x: random.choice(t.dictionary[x]), french));

  if(v): print "Writing translations to '../output0/translations0.txt'..."
  outputJoin(zip(translations, map(lambda x: x[1], dev)), "../output0/translations0.txt")
  printReport(dev);



def oneStrategyTranslations(v):
  if(v): print "\nStarting up the Translator for stage 1...";

  if(v): print "Reordering translations based on unweighted Part-Of-Sentence...";
  if(t == None): t = Translator();

  if(v): print "Reordering sentences based on grammar rules...";
  dev = readJoinFile(t.devFrenchFilename, t.devEnglishFilename);
  sentences = t.reorderTargets(map(lambda x: x[0], dev), False);
  dev = zip(sentences, map(lambda x: x[1], dev));

  translations = [];
  for french, english in dev:
    translations.append(map(lambda x: random.choice(t.dictionary[x]), french));

  if(v): print "Writing translations to '../output1/translations1.txt'..."
  outputJoin(zip(translations, map(lambda x: x[1], dev)), "../output0/translations1.txt")
  printReport(dev);



def twoStrategyTranslations(v):
  if(v): print "\nStarting up the Translator for stage 2...";

  if(v): print "Reordering translations based on weighted Part-Of-Sentence...";
  if(t == None): t = Translator();

  if(v): print "Training Structural Classifier..."
  t.trainStructuralClassifier();

  if(v): print "Reordering sentences based on classifier and grammar rules...";
  dev = readJoinFile(t.devFrenchFilename, t.devEnglishFilename);
  sentences = t.reorderTargets(map(lambda x: x[0], dev), True);
  dev = zip(sentences, map(lambda x: x[1], dev));

  translations = [];
  for french, english in dev:
    translations.append(map(lambda x: random.choice(t.dictionary[x]), french));

  if(v): print "Writing translations to '../output2/translations2.txt'..."
  outputJoin(zip(translations, map(lambda x: x[1], dev)), "../output2/translations2.txt")
  printReport(dev);



def threeStrategyTranslations(v):
  if(v): print "\nStarting up the Translator for stage 3...";

  if(v): print "Reordering translations based on weighted POS and Phrase Translation...";
  if(t == None): t = Translator();
  dev = readJoinFile(t.devFrenchFilename, t.devEnglishFilename);

  if(v): print "Training Structural Classifier..."
  if(t.structuralClassifier != None): t.trainStructuralClassifier();

  if(v): print "Initializing and Training Phrase Translator..."
  t.initializePhraseTranslator();

  if(v): print "Marking Detected Phrases...";
  dev = t.markPhrases(dev);

  if(v): print "Reordering sentences based on classifier and grammar rules...";
  sentences = t.reorderTargets(map(lambda x: x[0], dev), True);
  dev = zip(sentences, map(lambda x: x[1], dev));

  translations = [];
  for french, english in dev:
    translations.append(map(lambda x: random.choice(t.dictionary[x]) if not t.markedPhrase else t.translatePhrase(x), french));

  if(v): print "Writing translations to '../output3/translations3.txt'..."
  outputJoin(zip(translations, map(lambda x: x[1], dev)), "../output3/translations3.txt")
  printReport(dev);

# TODO
def fourStrategyTranslations(v):
  if(v): print "\nStarting up the Translator for stage 4...";
  if(v): print "Reordering translations based on weighted POS and Phrase Translation...";
  if(t == None): t = Translator();
  if(v): print "Training Structural Classifier..."
  t.trainStructuralClassifier();
  if(v): print "Reordering sentences based on classifier and grammar rules...";

  dev = readJoinFile(t.devFrenchFilename, t.devEnglishFilename);
  sentences = t.reorderTargets(map(lambda x: x[0], dev), True);
  dev = zip(sentences, map(lambda x: x[1], dev));

  translations = [];
  for french, english in dev:
    translations.append(map(lambda x: random.choice(t.dictionary[x]), french));

  if(v): print "Writing translations to '../output3/translations3.txt'..."
  outputJoin(zip(translations, map(lambda x: x[1], dev)), "../output3/translations3.txt")
  printReport(dev);

def fiveStrategyTranslations(v):
  if(v): print "Starting up the Translator for stage 5...";
  t = Translator();
  t.trainStructuralClassifier();
  t.trainDTClassifier();

def sixStrategyTranslations(v):
  if(v): print "Starting up the Translator for stage 6...";
  t = Translator();
  t.trainStructuralClassifier();
  t.trainDTClassifier();



def main():
  start = time.time();

  if(len(filter(lambda x: "-" not in x, sys.argv[1:])) == 0): throwError("Incorrect calling of directmt.py. See README.md for documentation.", True);

  shouldTime = reduce(lambda a,d: a or d == "-t", sys.argv[1:], False);
  verbose = reduce(lambda a,d: a or d == "-v", sys.argv[1:], False);

  
  m = {0:"zero", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six"};
  for i in sys.argv[1:]:
    if(i == "all"):
      for key in m:
        eval(m[key] + "StrategyTranslations(verbose);");
      break;

    elif("-" not in i):
      eval(m[i] + "StrategyTranslations(verbose);")

  if(shouldTime): print '\n\033[92m' + "Finished in ", int(time.time() - start)/100/10.0, "seconds!" + '\033[0m\n';
  sys.exit();

# Boilerplate
if __name__ == "__main__":
        main();