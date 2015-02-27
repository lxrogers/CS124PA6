
#!/usr/bin/env python
# Cayman Simpson (cayman@stanford.edu)
# CS124, Created: 22 February 2015
# file: PhraseTranslator.py
# 
# CS124 Homework 6 Direct Machine Translation, Phrase Translator
import collections
from nltk.tag.stanford import POSTagger
import re

# TODO: Cayman
class PhraseTranslator:

    def __init__(self, dictionary, POSClassifier):
        self.okWords = dictionary; # Translated phrases have to contain these words
        self.POSClassifier = POSClassifier;
        self.files = [("../data/parliament_french.txt", "../data/parliament_english.txt")];
        self.ngramCounts = collections.defaultdict(lambda: 0);
        self.probs = {};

        self.init();

    def init(self):
        with open(self.files[0][0]) as f:
            corpus = re.sub("(&quot;)|(&apos;)|$|%", "", f.read());
            # corpus = re.sub("-"," - ", corpus);
            # corpus = re.sub("\'"," \' ", corpus);
            corpus = map(lambda x: re.split("[\"\ \,\.\!\?\(\)]", x, re.UNICODE), re.split("\n", corpus));
            corpus = filter(lambda z: len(z) > 0, map(lambda x: filter(lambda y: len(y) > 0 and not y.isdigit(), x), corpus));

            self.train(corpus)

    def train(self, corpus):
        for sentence in corpus:

            #for every possible gram-length in the sentence
            for gramlength in xrange(1,7):

                #iterate through all possible grams of that gramlength
                for i in xrange(len(sentence) - gramlength):
                    #generate tuple
                    key = ();
                    for index in xrange(gramlength):
                        key += (sentence[i + index].lower(),);

                    self.ngramCounts[key] += 1;

        total = len(set(map(lambda tup: tup[0], self.ngramCounts)));

        grams = filter(lambda y: self.ngramCounts[y] > total*.001 and len(filter(lambda x: "-" not in x and "'" not in x ,y)) > 1, self.ngramCounts);

        # Frequentist Itemset Algorithm
        # 
        # Phrase must have appeared more than 20 times and must have a Bayesian Probability >= .6
        grams = map(lambda x: (x, float(self.ngramCounts[x])/self.ngramCounts[x[:-1]]), grams);
        grams = filter(lambda x: x[1] >= .6, grams);

        for x in grams:
            self.probs[x[0]] = x[1];

    def printPhrases(self):
        grams = map(lambda x: (x, self.probs[x]), self.probs);
        print sorted(grams, key=lambda x:x[1], reverse=True);

    def markPhrases(self, sentences):
        return [self.markPhrase(sentence) for sentence in sentences];


    def markPhrase(self, sentence):

        for l in range(2, len(sentence)):
            length = len(sentence) - l; # length of n-gram

            for index in range(l): # for the starting possible positions

                key = tuple(sentence[index:index+length]); # get the key of that length
                if(tuple(map(lambda x: x.lower(), key)) in self.probs): #if that is a phrase, mark it
                    sentence = sentence[:index] + ["<PHRASE>" + " ".join(key) + "</PHRASE>"]  + sentence[index+length:];

        sentence = filter(lambda x: len(x) > 0, sentence);
        return sentence;


    def isMarkedPhrase(self, token):
        return "<PHRASE" in token;

    #TODO:
    def translatePhrase(self, token):
        token = re.sub("(<PHRASE>)|(</PHRASE)","", token);
        return token;


def main():
    pt = PhraseTranslator({});
    pt.init();
    sentences = "";
    with open("../data/corpus/corpus_train.txt") as f:
            sentences = re.sub("(&quot;)|(&apos;)|$|%", "", f.read());
            sentences = re.sub("-"," - ", sentences);
            sentences = re.sub("\'"," \' ", sentences);
            sentences = map(lambda x: re.split("[\"\ \,\.\!\?\(\)]", x, re.UNICODE), re.split("\n", sentences));

    print pt.markPhrases(sentences);


    #pt.printPhrases();

# Boilerplate
if __name__ == "__main__":
        main();