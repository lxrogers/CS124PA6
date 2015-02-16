import sys
import getopt
import os
import collections
import math

class NaiveBayes:
    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
        """
        def __init__(self):
            self.train = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'pos' or 'neg' by convention.
             words is a list of strings.
        """
        def __init__(self):
            self.klass = ''
            self.words = []


    def __init__(self):
        """NaiveBayes initialization"""
        self.FILTER_STOP_WORDS = False
        self.BOOLEAN_NB = False
        self.stopList = set(self.readFile('../data/english.stop'))
        self.numFolds = 10
        self.posDoc = collections.defaultdict(lambda: 0);
        self.negDoc = collections.defaultdict(lambda: 0);
        self.docClass = [];

    #############################################################################
    # TODO TODO TODO TODO TODO 
    # Implement the Multinomial Naive Bayes classifier and the Naive Bayes Classifier with
    # Boolean (Binarized) features.
    # TODO: If the BOOLEAN_NB flag is true, your methods must implement Boolean (Binarized)
    # Naive Bayes (that relies on feature presence/absence) instead of the usual algorithm
    # that relies on feature counts

    def classify(self, words):
        if(self.BOOLEAN_NB): words = list(set(words));

        v = len(set(
          map(lambda x: x, self.posDoc) + map(lambda x: x, self.negDoc)
        ));

        priorPos = float(len(filter(lambda x: x == 'pos', self.docClass)))/len(self.docClass);
        priorNeg = 1 - priorPos;

        posSize = reduce(lambda a, d: a + self.posDoc[d], self.posDoc, 0);
        negSize = reduce(lambda a, d: a + self.negDoc[d], self.negDoc, 0);

        ps = math.log(priorPos);
        ns = math.log(priorNeg);
        for word in words:
            ps += math.log( (1 + float(self.posDoc[word]))/(posSize + v) );
            ns += math.log( (1 + float(self.negDoc[word]))/(negSize + v) );


        return 'pos' if ps > ns else 'neg'
    

    def addExample(self, klass, words):
        self.docClass += [klass];

        if(self.BOOLEAN_NB): words = list(set(words));

        for word in words:
            if(klass == 'pos'): 
               self.posDoc[word] += 1
            else:
                self.negDoc[word] += 1

            

    # END TODO (Modify code beyond here with caution)
    #############################################################################
    
    
    def readFile(self, fileName):
        """
         * Code for reading a file.    you probably don't want to modify anything here, 
         * unless you don't like the way we segment files.
        """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents)) 
        return result

    
    def segmentWords(self, s):
        """
         * Splits lines on whitespace for file reading
        """
        return s.split()

    
    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        for fileName in posTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            example.klass = 'neg'
            split.train.append(example)
        return split

    def train(self, split):
        for example in split.train:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words =    self.filterStopWords(words)
            self.addExample(example.klass, words)

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = [] 
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        #for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            splits.append(split)
        return splits


    def test(self, split):
        """Returns a list of labels for split.test."""
        labels = []
        for example in split.test:
            words = example.words
            if self.FILTER_STOP_WORDS:
                words =    self.filterStopWords(words)
            guess = self.classify(words)
            labels.append(guess)
        return labels
    
    def buildSplits(self, args):
        """Builds the splits for training/testing"""
        trainData = [] 
        testData = []
        splits = []
        trainDir = args[0]
        if len(args) == 1: 
            print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

            posTrainFileNames = os.listdir('%s/pos/' % trainDir)
            negTrainFileNames = os.listdir('%s/neg/' % trainDir)
            for fold in range(0, self.numFolds):
                split = self.TrainSplit()
                for fileName in posTrainFileNames:
                    example = self.Example()
                    example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                    example.klass = 'pos'
                    if fileName[2] == str(fold):
                        split.test.append(example)
                    else:
                        split.train.append(example)
                for fileName in negTrainFileNames:
                    example = self.Example()
                    example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                    example.klass = 'neg'
                    if fileName[2] == str(fold):
                        split.test.append(example)
                    else:
                        split.train.append(example)
                splits.append(split)
        elif len(args) == 2:
            split = self.TrainSplit()
            testDir = args[1]
            print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
            posTrainFileNames = os.listdir('%s/pos/' % trainDir)
            negTrainFileNames = os.listdir('%s/neg/' % trainDir)
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                split.train.append(example)

            posTestFileNames = os.listdir('%s/pos/' % testDir)
            negTestFileNames = os.listdir('%s/neg/' % testDir)
            for fileName in posTestFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (testDir, fileName)) 
                example.klass = 'pos'
                split.test.append(example)
            for fileName in negTestFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (testDir, fileName)) 
                example.klass = 'neg'
                split.test.append(example)
            splits.append(split)
        return splits
    
    def filterStopWords(self, words):
        """Filters stop words."""
        filtered = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                filtered.append(word)
        return filtered

def test10Fold(args, FILTER_STOP_WORDS):
    nb = NaiveBayes()
    splits = nb.buildSplits(args)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayes()
        accuracy = 0.0
        for example in split.train:
            words = example.words
            if FILTER_STOP_WORDS:
                words =    classifier.filterStopWords(words)
            classifier.addExample(example.klass, words)
    
        for example in split.test:
            words = example.words
            if FILTER_STOP_WORDS:
                words =    classifier.filterStopWords(words)
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy
        
        
def classifyFile(FILTER_STOP_WORDS, trainDir, testFilePath):
    classifier = NaiveBayes()
    classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
    trainSplit = classifier.trainSplit(trainDir)
    classifier.train(trainSplit)
    testFile = classifier.readFile(testFilePath)
    print classifier.classify(testFile)
        
def main():
    FILTER_STOP_WORDS = False
    (options, args) = getopt.getopt(sys.argv[1:], 'f')
    if ('-f','') in options:
        FILTER_STOP_WORDS = True
    
    if len(args) == 2 and os.path.isfile(args[1]):
        classifyFile(FILTER_STOP_WORDS, args[0], args[1])
    else:
        test10Fold(args, FILTER_STOP_WORDS)

if __name__ == "__main__":
        main()
