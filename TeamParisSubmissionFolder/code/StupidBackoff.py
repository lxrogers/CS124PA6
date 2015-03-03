import math, collections

class StupidBackoffLanguageModel:
    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.ngramCounts = collections.defaultdict(lambda: 0);
        self.probs = {};
        self.total = 0;
        self.maxLength = 0;
        self.train(corpus)

    def train(self, corpus):

        #TODO: implement bayes rule
        """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
        """  
        # Generate all possible n-grams
        # for every sentence in the corpus
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

        self.total = len(set(map(lambda tup: tup[0], self.ngramCounts)));

        self.maxLength = max(map(lambda tup: len(tup), self.ngramCounts));

        grams = filter(lambda y: self.ngramCounts[y] > self.total*.001 and len(filter(lambda x: "-" not in x and "'" not in x ,y)) > 1, self.ngramCounts);

        # Frequentist Itemset Algorithm
        # 
        # Phrase must have appeared more than 20 times and must have a Bayesian Probability >= .6
        grams = map(lambda x: (x, float(self.ngramCounts[x])/self.ngramCounts[x[:-1]]), grams);
        grams = filter(lambda x: x[1] >= .6, grams);

        for x in grams:
            self.probs[x[0]] = x[1];
       

    def getBackOff(self, key):
        if(len(key) <= 1): # at the end and have a ngram of length one
            return float(self.ngramCounts[key])/(self.total);
        elif(key in self.ngramCounts): # we found the right ngram
            return float(self.ngramCounts[key])/self.ngramCounts[key[:-1]];
        else: # we need to backoff
            return .4*self.getBackOff(key[1:]);

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
            sentence using your language model. Use whatever data you computed in train() here.
        """
        s = 0;

        #for every word
        for i in xrange(len(sentence)):
            score =  self.getBackOff(tuple(sentence[:i+1]));
            if(score != 0):
                s += math.log(score);


        return s

    def printScores(self):
        grams = map(lambda x: (x, self.probs[x]), self.probs);
        print sorted(grams, key=lambda x:x[1], reverse=True);




