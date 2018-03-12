#SGD calls everything as a single class sometimes because the test data is too small wrt training data and we are using a binary classifier
#lack of data may result in volatility of accuracy
from nltk.classify.scikitlearn import SklearnClassifier
import nltk
import random
from nltk.corpus import movie_reviews
import pickle
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize
from statistics import mode
#we can inherit from the Classifier class


class VoteClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers = classifiers
        #classifiers is a list of all the classifiers
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

#Multinomial distribution not binary
#changing the default parameters of these algorithms can increase the success rate by about 10%
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


short_pos = open('positive.txt','r').read()
short_neg = open('negative.txt','r').read()


##classifier_f = open('documents.pickle','rb')
##documents = pickle.load(classifier_f)
##classifier_f.close()
documents = []
all_words = []
#  j is adject, r is adverb, and v is verb
#allowed_word_types = ["J","R","V"]


classifier_f = open('doc.pickle','rb')
documents = pickle.load(classifier_f)
classifier_f.close()


classifier_f = open('word_features.pickle','rb')
word_features = pickle.load(classifier_f)
classifier_f.close()



def find_features(documents):
    words = word_tokenize(documents)
    #documents was a string
    features = {}
    for w in word_features:
        features[w] = (w in words)
    #if w is in documents
    return features

classifier_f = open('featuresets.pickle','rb')
featuresets = pickle.load(classifier_f)
classifier_f.close()



random.shuffle(featuresets)

training_set = featuresets[:10000]
testing = featuresets[10000:]

classifier_f = open('naivebayes.pickle','rb')
classifier = pickle.load(classifier_f)
classifier_f.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
classifier_f = open('MNB.pickle','rb')
MNB_classifier = pickle.load(classifier_f)
classifier_f.close()


Bernoulli_classifier = SklearnClassifier(BernoulliNB())
classifier_f = open('Bernoulli.pickle','rb')
Bernoulli_classifier = pickle.load(classifier_f)
classifier_f.close()


LR_classifier = SklearnClassifier(LogisticRegression())
classifier_f = open('LR.pickle','rb')
LR_classifier = pickle.load(classifier_f)
classifier_f.close()

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
classifier_f = open('SGD.pickle','rb')
SGDClassifier_classifier = pickle.load(classifier_f)
classifier_f.close()

LinearSVC_classifier = SklearnClassifier(LinearSVC())
classifier_f = open('LinearSVC.pickle','rb')
LinearSVC_classifier = pickle.load(classifier_f)
classifier_f.close()

NuSVC_classifier = SklearnClassifier(NuSVC())
classifier_f = open('NuSVC.pickle','rb')
NuSVC_classifier = pickle.load(classifier_f)
classifier_f.close()

voted_classifier = VoteClassifier(classifier,MNB_classifier,Bernoulli_classifier,LR_classifier,SGDClassifier_classifier,LinearSVC_classifier,NuSVC_classifier)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
