#! /usr/local/bin/python
# Andrew Mather, Cayman Simpson, Lawrence Rogers, Raissa Largman
# CS124, Created: 17 February 2015
# file: directmt.py

# The purpose of this file is to use direct machine translation
# to translate a small corpus of sentences using techniques
# learned in CS124.
# 
# NOTE: Dependency: nltk package, JDK 8 and python 2.7

# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join
import time
import random
from nltk.tag.stanford import POSTagger
from PhraseTranslator import PhraseTranslator
from NaiveBayes import NaiveBayes
import re
import codecs
from WordSelector import WordSelector

# GLOBAL
t = None;

class Translator:

    def __init__(self):
      self.dicFilename = "../data/dictionary.txt";
      self.dictionary = {};
      self.readDictionary(self.dicFilename);

      self.trainFilename = "";

      self.devFrenchFilename = "../data/corpus/corpus_train.txt";
      self.devEnglishFilename = "../data/human_translation_corpus.txt";

      self.testFrenchFilename = "../data/corpus/corpus_test.txt";
      self.testEnglishFilename = "../data/google_translate/google_translate_corpus_test.txt";

      self.targetSentences = [];

      self.POSClassifier = POSTagger(
        'stanford-postagger/models/french.tagger', 
        'stanford-postagger/stanford-postagger.jar',
        'utf-8'
      )
      self.EnglishPOSClassifier = POSTagger(
        'stanford-postagger/models/english-bidirectional-distsim.tagger', 
        'stanford-postagger/stanford-postagger.jar',
        'utf-8'
      )
      self.structuralClassifier = NaiveBayes();
      self.phraseTranslator = PhraseTranslator(self.dictionary, self.POSClassifier);
      self.selector = WordSelector(self.POSClassifier)
      self.selector.trainOnDictionary(self.dictionary)

    def readDictionary(self, filename):
      self.dictionary = {};
      with open(filename) as f:
        for line in f:
          if(":" not in line): continue;
          self.dictionary[line.split(":")[0].lower()] = map(lambda x: x.strip(), line.split(":")[1].split(","));

    def readJoinFiles(self, file1, file2):
      return zip(readFile(file1).split("\n"), readFile(file2).split("\n"));

    # Read in StatMT data and then train the differences between english and french among translations

    def trainStructuralClassifier(self):
      FRENCH_PARLIAMENT_FILEPATH = '../data/parliament_french.txt'
      ENGLISH_PARLIAMENT_FILEPATH = '../data/parliament_english.txt'

      frenchPOSTrainData = self.POSClassifier.tag_sents(
        readFile(FRENCH_PARLIAMENT_FILEPATH).split("\n")
      )
      englishPOSTrainData = self.EnglishPOSClassifier.tag_sents(
        readFile(ENGLISH_PARLIAMENT_FILEPATH).split("\n")
      )
      self.structuralClassifier.addExamples(frenchPOSTrainData, englishPOSTrainData)


    def trainLanguageModel(self):
      self.selector.setDictionary(self.dictionary)
      self.selector.train()

    def translate(self):
      pass; #reorder sentence, validate

    def isNoun(self, pos):
      return pos == "NPP" or pos == "NC" or pos == "CLS" or pos == "N"

    def reorderTargets(self, sentences, level):
      # adjectives nouns switch
      # pronouns switch order
      # preprocess sentences 

      
      pos_sentences = self.POSClassifier.tag_sents(sentences);
      ret = [];

      #put phrases back
      for i in range(len(pos_sentences)):
        temp = [];
        inPhrase = False;
        start = 0;
        for j in range(len(pos_sentences[i])):
          if "<PHRASE>" in pos_sentences[i][j][0]:
            inPhrase = True;
            start = j
            print pos_sentences[i][j][0], start
          if not inPhrase:
            temp.append(pos_sentences[i][j]);
          if "</PHRASE>" in pos_sentences[i][j][0]:
            key = "";
            for k in range(start, j + 1):
              key += pos_sentences[i][k][0] + " ";
            temp.append((key, ''));
            inPhrase = False;
        pos_sentences[i] = temp;

      print pos_sentences
      for sent in pos_sentences:
        for i in range(len(sent)):
          word = sent[i][0];
          pos = sent[i][1];
          if(pos == "ADJ" and i != 0 and self.isNoun(sent[i-1][1]) and pos and level > 1):
            #switch adjective nouns
            print "REORDERING: ", sent[i-1][0], word
            sent[i-1], sent[i] = sent[i], sent[i-1]

          if(pos == "ADJ" and i > 1 and sent[i-1][1] == "ADV" and self.isNoun(sent[i-2][1]) and level > 1):
            # noun adverb adj => adverb, adj noun
            print "REORDERING: ", sent[i-2][0], sent[i-1][0], word
            sent[i-2], sent[i-1], sent[i] = sent[i-1], sent[i], sent[i-2];

          if(self.isNoun(pos) and i < len(sent) - 2 and sent[i+1][1] == "CLO" and sent[i+2][1] == "V" and level > 2): #pronouns
            #noun pronoun, verb -> noun verb pronoun
            print "REORDERING: ", word, sent[i+1][0], sent[i+2][0]
            sent[i+1], sent[i+2] = sent[i+2], sent[i+1];

          if(word == "ne" and level > 3):
            # deleting ne and replacing it with pas
            print "CLEANING: ", sent[i][0], sent[i+1][0], sent[i+2][0];
            if(i < len(sent) - 2 and sent[i+2][0] == 'pas'): sent[i], sent[i+2] = ('pas', ''), ('','');
            else: sent[i] = ('','');

          if(pos == "VINF" and i > 0 and sent[i-1][1] == "CLO" and level > 4):
            # switch pronoun infverb => infverb pronoung
            print "REORDERING: ", sent[i-1][0], word
            sent[i-1], sent[i] = sent[i], sent[i-1]
          
        #int "All of sent %s" % sent
        ret.append(map(lambda x: x, sent));

        #print ret[len(ret) - 1]

      return ret; #weighted would have classifier

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

    def replace(self, sentences, match, replace):
      index = sentences.find(match);
      while(index != -1):
        sentences = sentences[:index] + replace + sentences[index + len(match):];
        index = sentences.find(match, index);
      return sentences;

    def preprocess(self, sentences):
      sentences = self.replace(sentences, "J'", "Je ");
      sentences = self.replace(sentences, "m'", "me ");
      sentences = self.replace(sentences, "j'", "je ");
      sentences = self.replace(sentences, "l'", "le ");
      sentences = self.replace(sentences, "L'", "Le ");
      sentences = self.replace(sentences, "t'", "te ");
      sentences = self.replace(sentences, "c'", "ce ");
      sentences = self.replace(sentences, "C'", "Ce ");
      sentences = self.replace(sentences, "n'", "ne ");
      return sentences;




##############################################################################################################################
##############################################################################################################################
#################################################### UTILITY FUNCTIONS #######################################################
##############################################################################################################################
##############################################################################################################################

# Reads a file and returns the text contents
def readFile(filename):
  with open(filename) as f: return f.read();

def readJoinFile(filename1, filename2):
  return zip(readFile(filename1).split("\n"), readFile(filename2).split("\n"));

def readFileUTF(filename):
  with codecs.open(filename,'r',encoding='utf8') as f:
    return f.read();

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
      w.write(str(tup[0]) + "\n" + str(tup[1]) + "\n\n");
      print "TRANSLATION: " + str(tup[0]) + "\nENGLISH: " + str(tup[1]) + "\n\n"
    w.close();  
  except IOError:
    print "Could not write translation to '" + filename + "'."; 

#print report of sentences
def printReport(translations, dev):
  for i in range(len(dev)):
    print "TRANSLATION: ", translations[i];
    print "ENGLISH:     ", dev[i][1];
    print "\n";

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


def zeroStrategyTranslations(v, test):
  global t;

  if(v): print "\nStarting up the Translator for stage 0...";
  if(v): print "Random Direct Machine Translation...";
  t = Translator();

  if(v): print "Translating Sentences...";
  if test:
    dev = readJoinFile(t.testFrenchFilename, t.testEnglishFilename)
  else:
    dev = readJoinFile(t.devFrenchFilename, t.devEnglishFilename);
  translations = [];
  for french, english in dev:
    french = filter(lambda x: len(x) > 0, re.split("[\"\ \'\,\.\!\?\(\)]", french));
    translations.append(map(lambda x: random.choice(t.dictionary[x.lower()]) if x in t.dictionary else x, french));

  translations = map(lambda x: " ".join(x), translations);

  if(v): print "Writing translations to '../output0/translations0.txt'..."
  outputJoin(zip(translations, map(lambda x: x[1], dev)), "../output0/translations0.txt")



def oneStrategyTranslations(v, test):
  global t;

  if(v): print "\nStarting up the Translator for stage 1...";

  if(v): print "Translating with Naive Bayes classifier...";
  if(t == None): t = Translator();

  if(v): print "Reordering sentences based on grammar rules...";
  if test:
    sentences = readFile(t.testFrenchFilename)
  else:
    sentences = readFile(t.devFrenchFilename);
  # sentences = re.sub("-"," - ", sentences);
  # sentences = re.sub("\'"," \' ", sentences);
  sentences = t.preprocess(sentences);
  sentences = map(lambda x: re.split("[\"\'\ \,\.\!\?\(\)]", x), re.split("\n", sentences));
  
  sentences = t.reorderTargets(sentences, 1); # does nothing

  translations = [];
  for french in sentences:
    french = filter(lambda x: len(x[0]) > 0, french);
    translations.append(map(lambda x: t.selector.chooseWord([x[0].lower().encode('utf-8'), x[1].encode('utf-8')]) if x[0].lower().encode('utf-8') in t.dictionary else x[0].encode('utf-8'), french));

  if(v): print "Writing translations to '../output1/translations1.txt'..."

  if test:
     outputJoin(zip(translations, readFile(t.testEnglishFilename).split("\n")), "../output1/translations1.txt")
  else:
    outputJoin(zip(translations, readFile(t.devEnglishFilename).split("\n")), "../output1/translations1.txt")



def twoStrategyTranslations(v, test):
  global t;

  if(v): print "\nStarting up the Translator for stage 2...";

  if(v): print "Reordering translations based on weighted Part-Of-Sentence...";
  if(t == None): t = Translator();

  if(v): print "Reordering sentences based on grammar rules...";
  if test:
    sentences = readFile(t.testFrenchFilename)
  else:
    sentences = readFile(t.devFrenchFilename);
  # sentences = re.sub("-"," - ", sentences);
  # sentences = re.sub("\'"," \' ", sentences);
  sentences = t.preprocess(sentences);
  sentences = map(lambda x: re.split("[\"\'\ \,\.\!\?\(\)]", x), re.split("\n", sentences));
  
  sentences = t.reorderTargets(sentences, 2);

  translations = [];
  for french in sentences:
    french = filter(lambda x: len(x[0]) > 0, french);
    translations.append(map(lambda x: t.selector.chooseWord([x[0].lower().encode('utf-8'), x[1].encode('utf-8')]) if x[0].lower().encode('utf-8') in t.dictionary else x[0].encode('utf-8'), french));

  if(v): print "Writing translations to '../output2/translations2.txt'..."

  if test:
     outputJoin(zip(translations, readFile(t.testEnglishFilename).split("\n")), "../output2/translations2.txt")
  else:
    outputJoin(zip(translations, readFile(t.devEnglishFilename).split("\n")), "../output2/translations2.txt")



def threeStrategyTranslations(v, test):
  global t;
  if(v): print '\n\033[94m' + "\nStarting up the Translator for stage 3..." + '\033[0m\n';

  if(v): print "Reordering translations based on weighted POS...";
  if(t == None): t = Translator();

  if test:
    sentences = readFile(t.testFrenchFilename)
  else:
    sentences = readFile(t.devFrenchFilename);

  sentences = t.preprocess(sentences);
  sentences = map(lambda x: re.split("[\"\'\ \,\.\!\?\(\)]", x), re.split("\n", sentences)); 

  # if(v): print "Training Structural Classifier..."
  # if(t.structuralClassifier != None): t.trainStructuralClassifier();

  if(v): print "Reordering sentences based on classifier and grammar rules...";
  sentences = t.reorderTargets(sentences, 3);

  translations = [];
  for french in sentences:
    french = filter(lambda x: len(x[0]) > 0, french);
    translations.append(map(lambda x: t.selector.chooseWord([x[0].lower().encode('utf-8'), x[1].encode('utf-8')]), french));

  if(v): print "Writing translations to '../output3/translations3.txt'..."

  if test:
    outputJoin(zip(translations, readFile(t.testEnglishFilename).split("\n")), "../output3/translations3.txt")
  else:
    outputJoin(zip(translations, readFile(t.devEnglishFilename).split("\n")), "../output3/translations3.txt")

def fourStrategyTranslations(v, test):
  global t;
  if(v): print '\n\033[94m' + "\nStarting up the Translator for stage 4..." + '\033[0m\n';

  if(v): print "Reordering translations based on weighted POS...";
  if(t == None): t = Translator();

  if test:
    sentences = readFile(t.testFrenchFilename)
  else:
    sentences = readFile(t.devFrenchFilename);

  sentences = t.preprocess(sentences);
  sentences = map(lambda x: re.split("[\"\'\ \,\.\!\?\(\)]", x), re.split("\n", sentences)); 

  # if(v): print "Training Structural Classifier..."
  # if(t.structuralClassifier != None): t.trainStructuralClassifier();

  if(v): print "Reordering sentences based on classifier and grammar rules...";
  sentences = t.reorderTargets(sentences, 4);

  translations = [];
  for french in sentences:
    french = filter(lambda x: len(x[0]) > 0, french);
    translations.append(map(lambda x: t.selector.chooseWord([x[0].lower().encode('utf-8'), x[1].encode('utf-8')]), french));

  if(v): print "Writing translations to '../output5/translations5.txt'..."

  if test:
    outputJoin(zip(translations, readFile(t.testEnglishFilename).split("\n")), "../output4/translations4.txt")
  else:
    outputJoin(zip(translations, readFile(t.devEnglishFilename).split("\n")), "../output4/translations4.txt")

def fiveStrategyTranslations(v, test):
  global t;
  if(v): print '\n\033[94m' + "\nStarting up the Translator for stage 5..." + '\033[0m\n';

  if(v): print "Reordering translations based on weighted POS...";
  if(t == None): t = Translator();

  if test:
    sentences = readFile(t.testFrenchFilename)
  else:
    sentences = readFile(t.devFrenchFilename);

  sentences = t.preprocess(sentences);
  sentences = map(lambda x: re.split("[\"\'\ \,\.\!\?\(\)]", x), re.split("\n", sentences)); 

  # if(v): print "Training Structural Classifier..."
  # if(t.structuralClassifier != None): t.trainStructuralClassifier();

  if(v): print "Reordering sentences based on classifier and grammar rules...";
  sentences = t.reorderTargets(sentences, 5);

  translations = [];
  for french in sentences:
    french = filter(lambda x: len(x[0]) > 0, french);
    translations.append(map(lambda x: t.selector.chooseWord([x[0].lower().encode('utf-8'), x[1].encode('utf-8')]), french));

  if(v): print "Writing translations to '../output5/translations5.txt'..."

  if test:
    outputJoin(zip(translations, readFile(t.testEnglishFilename).split("\n")), "../output5/translations5.txt")
  else:
    outputJoin(zip(translations, readFile(t.devEnglishFilename).split("\n")), "../output5/translations5.txt")

def sixStrategyTranslations(v, test):
  global t;
  if(v): print '\n\033[94m' + "\nStarting up the Translator for stage 6..." + '\033[0m\n';

  if(v): print "Reordering translations based on weighted POS and Phrase Translation...";
  if(t == None): t = Translator();

  if test:
    sentences = readFile(t.testFrenchFilename)
  else:
    sentences = readFile(t.devFrenchFilename);

  sentences = t.preprocess(sentences);
  sentences = map(lambda x: re.split("[\"\'\ \,\.\!\?\(\)]", x), re.split("\n", sentences)); 

  # if(v): print "Training Structural Classifier..."
  # if(t.structuralClassifier != None): t.trainStructuralClassifier();

  if(v): print "Marking Detected Phrases...";
  sentences = t.markPhrases(sentences);

  if(v): print "Reordering sentences based on classifier and grammar rules...";
  sentences = t.reorderTargets(sentences, 6);

  translations = [];
  for french in sentences:
    french = filter(lambda x: len(x[0]) > 0, french);
    translations.append(map(lambda x: t.selector.chooseWord([x[0].lower().encode('utf-8'), x[1].encode('utf-8')]) if not t.markedPhrase(x[0]) else t.translatePhrase(x[0]), french));

  if(v): print "Writing translations to '../output3/translations3.txt'..."

  if test:
    outputJoin(zip(translations, readFile(t.testEnglishFilename).split("\n")), "../output6/translations6.txt")
  else:
    outputJoin(zip(translations, readFile(t.devEnglishFilename).split("\n")), "../output6/translations6.txt")

def main():
  global t;
  start = time.time();


  if(len(filter(lambda x: "-" not in x, sys.argv[1:])) == 0): throwError("Incorrect calling of directmt.py. See README.md for documentation.", True);

  shouldTime = reduce(lambda a,d: a or d == "-t", sys.argv[1:], False);
  verbose = reduce(lambda a,d: a or d == "-v", sys.argv[1:], False);
  test = reduce(lambda a,d: a or d== "-e", sys.argv[1:], False);

  for i in sys.argv[1:]:
    if('all' in sys.argv[1:]):
      i = 'all';
    if(i == '0' or i == 'all'):
      zeroStrategyTranslations(verbose, test);
    if(i == '1' or i == 'all'):
      oneStrategyTranslations(verbose, test);
    if(i == '2' or i == 'all'):
      twoStrategyTranslations(verbose, test);
    if(i == '3' or i == 'all'):
      threeStrategyTranslations(verbose, test);
    if(i == '4' or i == 'all'):
      fourStrategyTranslations(verbose, test);
    if(i == '5' or i == 'all'):
      fiveStrategyTranslations(verbose, test);
    if(i == '6' or i == 'all'):
      sixStrategyTranslations(verbose, test);
    if(i == 'all'):
      break;


  if(shouldTime): print '\n\033[92m' + "Finished in ", int(time.time() - start), "seconds!" + '\033[0m\n';
  sys.exit();

# Boilerplate
if __name__ == "__main__":
        main();