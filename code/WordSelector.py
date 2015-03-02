# -*- coding: utf-8 -*-

import sys
import re
import random
import codecs
from NaiveBayes import NaiveBayes

class WordSelector:
	def __init__(self, POSClassifier):
		self.source = "../data/corpus/corpus_train.txt"

		self.ENGLISH_PARLIAMENT_FILEPATH = '../data/parliament_english.txt'
		self.FRENCH_PARLIAMENT_FILEPATH = '../data/parliament_french.txt'
		self.FRENCH_TAGGED_FILEPATH = '../data/tagged_parliament_french.txt'

		self.POSClassifier = POSClassifier

		self.classifier = NaiveBayes()
		self.dictionary = {'heures': ['time', 'hour'], 'pris': ['taken'], 'le': ['the', 'it', 'him'], 'manquer': ['miss', 'fail'], 'yeux': ['eyes'], 'alle': ['gone']}
		self.englishDictionary = {}

	def trainOnDictionary(self, dictionary):
		self.dictionary = dictionary
		self.train()

	#TODO Implement
	def stemWord(self, word):
		return word

	def computeMonogramFrequency(self):
		englishPOSTrainData = readFile(self.ENGLISH_PARLIAMENT_FILEPATH).split(" ")

		for idx, word in enumerate(englishPOSTrainData):
			if word not in self.englishDictionary:
				self.englishDictionary[word] = 1
			else:
				self.englishDictionary[word] += 1

	def trainClassifier(self):
		frenchPOSTrainData = readFile(self.FRENCH_TAGGED_FILEPATH).split("\n")
		englishPOSTrainData = readFile(self.ENGLISH_PARLIAMENT_FILEPATH).split("\n")

		classes = []
		features = []

		for fPost, ePost in zip(frenchPOSTrainData, englishPOSTrainData):
			frenchList = fPost.split(" ")

			for i, feature in enumerate(frenchList):
				components = feature.split("_")

				lowerFeature = components[0].lower()
				if lowerFeature not in self.dictionary or lowerFeature.strip() == "":
					continue

				engList = ePost.split(" ")

				for translation in self.dictionary[lowerFeature]:
					if translation in ePost:
						#if prevWord == "":
						translationFeatures = [lowerFeature, components[1]]
						#else:
							#bigramFeature = prevWord.upper() + "_PREV"
							#translationFeatures = [lowerFeature, bigramFeature]
			
						features.append(translationFeatures)
						classes.append(translation)

				prevWord = lowerFeature

		for fList, klass in zip(features, classes):
			pass

		self.classifier.addExamples(features, classes)

	def train(self):
		#self.computeBigramFrequency()
		self.trainClassifier()
		self.computeMonogramFrequency()


	def chooseWord(self, keys):
		print
		classification = self.classifier.classifyWithOptions(keys, self.dictionary[keys[0]])
			
		if classification != "NO LABEL":
			return classification

		topCount = 0
		topTranslation = ""

		for candidate in self.dictionary[keys[0]]:
			if candidate in self.englishDictionary:
				if self.englishDictionary[candidate] > topCount:
					topCount = self.englishDictionary[candidate]
					topTranslation = candidate
		if topTranslation == "":
			#Hopefully it won't come to this
			return random.choice(self.dictionary[keys[0]])+"_RAND"
		return topTranslation + "_PROB"

def readFile(filename):
	with open(filename,'r') as f:
		return f.read();

#Runs a series of quick tests
def main():
	ws = WordSelector()
	ws.train()
	for idx, key in enumerate(ws.dictionary):
		print "Key is %s" % key
		result = ws.chooseWord(key)
		print "Classifier returns %s" % result

if __name__ == '__main__':
    main();