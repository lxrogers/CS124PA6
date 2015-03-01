import sys
import random
import codecs
from NaiveBayes import NaiveBayes

class WordSelector:
	def __init__(self):
		self.source = "../data/corpus/corpus_train.txt"

		self.ENGLISH_PARLIAMENT_FILEPATH = '../data/parliament_english.txt'
		self.FRENCH_PARLIAMENT_FILEPATH = '../data/parliament_french.txt'

		self.classifier = NaiveBayes()
		self.dictionary = {'heures': ['time', 'hour'], 'pris': ['taken'], 'le': ['the', 'it', 'him'], 'manquer': ['miss', 'fail'], 'yeux': ['eyes'], 'alle': ['gone']}
		self.englishDictionary = {}
	
	#Used in "main" tests
	def getDictionary(self):
		return self.dictionary

	def setDictionary(self, dictionary):
		self.dictionary = dictionary

	#TODO Implement
	def stemWord(self, word):
		return word

	def computeMonogramFrequency(self):
		ENGLISH_PARLIAMENT_FILEPATH = '../data/parliament_english.txt'

		englishPOSTrainData = readFileUTF(ENGLISH_PARLIAMENT_FILEPATH).split(" ")

		for idx, word in enumerate(englishPOSTrainData):
			if word not in self.englishDictionary:
				self.englishDictionary[word] = 1
			else:
				self.englishDictionary[word] += 1

	def trainClassifier(self):
		frenchPOSTrainData = readFileUTF(self.FRENCH_PARLIAMENT_FILEPATH).split("\n")
		englishPOSTrainData = readFileUTF(self.ENGLISH_PARLIAMENT_FILEPATH).split("\n")

		classes = []
		features = []

		for fPost, ePost in zip(frenchPOSTrainData, englishPOSTrainData):
			frenchList = fPost.split(" ")
			prevWord = ""

			for i, feature in enumerate(frenchList):
				if feature not in self.dictionary:
					continue

				engList = ePost.split(" ")

				for translation in self.dictionary[feature]:
					if translation in engList:
						if prevWord == "":
							translationFeatures = [feature]
						else:
							bigramFeature = prevWord.upper() + "_PREV"
							translationFeatures = [feature, bigramFeature]
			
						features.append(translationFeatures)
						classes.append(translation)

				prevWord = feature

		for fList, klass in zip(features, classes):
			pass

		self.classifier.addExamples(features, classes)

	def train(self):
		#self.computeBigramFrequency()
		self.trainClassifier()
		self.computeMonogramFrequency()


	def chooseWord(self, word):
		keys = [word]
		classification = self.classifier.classifyWithOptions(keys, self.dictionary[word])
			
		if classification != "NO LABEL":
			return classification

		topCount = 0
		topTranslation = ""

		for candidate in self.dictionary[word]:
			if candidate in self.englishDictionary:
				if self.englishDictionary[candidate] > topCount:
					topCount = self.englishDictionary[candidate]
					topTranslation = candidate
		return topTranslation

#Stolen from directmt
def readFileUTF(filename):
  with codecs.open(filename,'r',encoding='utf8') as f:
  	return f.read();

#Runs a series of quick tests
def main():
	ws = WordSelector()
	ws.train()
	for idx, key in enumerate(ws.getDictionary()):
		print "Key is %s" % key
		result = ws.chooseWord(key)
		print "Classifier returns %s" % result

if __name__ == '__main__':
    main();