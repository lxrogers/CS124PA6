
#!/usr/bin/env python
# Cayman Simpson (cayman@stanford.edu)
# CS124, Created: 22 February 2015
# file: PhraseTranslator.py
# 
# CS124 Homework 6 Direct Machine Translation, Phrase Translator


# TODO: Cayman
class PhraseTranslator:

    def __init__(self, dictionary, POSClassifier):
        self.okWords = dictionary; # Translated phrases have to contain these words
        self.POSClassifier = POSClassifier;
        self.train();

    def train(self):
        pass;

    def markPhrases(self, sentences):
        return [self.markPhrase(sentence) for sentence in sentences];


    def markPhrase(self, sentence):
        return sentence;

    def isMarkedPhrase(self, token):
        return False;

    def translatePhrase(self, token):
        return "";

def main():
    pass;

# Boilerplate
if __name__ == "__main__":
        main();