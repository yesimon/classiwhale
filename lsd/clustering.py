# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import sys
# horrific path mangling here :(
sys.path.extend(['../dxm/', '../lib/'])

# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)


from status.models import Status
from twitterauth.models import Rating
import numpy as np
import scipy.cluster.hierarchy as hierarchy
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import nltk.metrics as metrics

from training import TrainingSet, TrainingUser
import status.management.commands.extract as extract
import cPickle
import pickle
import sys
import random
import collections
import bisect
import copy 

import cProfile

punctuation = ',.?;:"!\''



class CommonData():
    """ Elements in the dictionary 
    self.rating_data
    self.train_data
    self.word_dictionary
    self.rating_matrix
    self.tweets
    self.raters
    self.labelings
    self.corpus
    self.labels
    self.corpus_lookup
    self.labels_lookup
    """
                
    def __init__(self):
        commondata_filename = 'commondata.pkl'
        try:
            self._LoadData(commondata_filename)
        except IOError:
            self._AssembleData()
            self._FillData()
            self._StoreData(commondata_filename)
            
    def _LoadData(self, filename):
        with open(filename, 'r') as f:
            data = pickle.loads(f.read().replace('\r\n', '\n'))
        self.__dict__ = data.__dict__
                
    def _StoreData(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self, f)

    def _AssembleData(self):
        """Assemble a bunch of data, assembles data from other pickled files
        for efficiency"""
        ratings_filename = 'train_set_dump.pkl'
        tweets_filename = 'train_set.pkl'
        tokens_filename = 'tweet_tokens.pkl'
        self.stopwords = stopwords.words('english')       
        with open(ratings_filename, 'r') as f: 
            self.rating_data = cPickle.load(f.read().replace('\r\n', '\n'))
        with open(tweets_filename, 'r') as f:
            self.train_data = cPickle.load(f.read().replace('\r\n', '\n'))
        try: 
            with open(tokens_filename, 'r') as f:
                self.word_dictionary = cPickle.load(f.read().replace('\r\n', '\n'))
        except IOError:
            self.word_dictionary = self.ExtractDictionary(self.train_set, self) 
            with open(tokens_filename, 'w') as f:
                cPickle.dump(self.word_dictionary, f)
    
    def _FillData(self):
        """Compute the rest of common data after loading as much as possible"""
        self.ratings_matrix = self.ExtractRatings(self.train_data, self.rating_data)
        self.num_raters = len(self.ratings_matrix)
        self.tweets = self.ExtractTweets(self.train_data)
        self.raters = sorted(self.rating_data.keys())
        self.corpus = {}
        self.labelings = [-1, 1]
        for i, word in enumerate(sorted(self.word_dictionary.keys())):
            self.corpus[word] = i
        self.labels = {}
        for i, label in enumerate(sorted(self.labelings)):
            self.labels[label] = i  
        self.num_tokens = len(self.corpus)
        self.corpus_lookup = sorted(self.corpus.keys())
        self.num_labels = len(self.labels)
        self.labels_lookup = sorted(self.labels)
        self.classifiers = self.TrainClassifiers()
 
    def TrainClassifiers(self):
        """Train classifiers for all raters"""
        classifiers = {}
        for i in range(len(self.raters)):
            user_ratings = self.rating_data[self.raters[i]]
            rating_ids = user_ratings.keys()
            trainfeats = CreateTrainingSet(self, rating_ids, user_ratings)
            classifier = MultinomialBayesClassifier(self)   
            classifier.train(trainfeats)         
            classifiers[i] = classifier
        return classifiers
        
    @staticmethod
    def ExtractTweets(train_data):
        """Extract all tweets in an id: dict('text', 'user') manner"""
        api_statuses = []
        tweets = {}
        for timeline in train_data.tweetdb.values():
            api_statuses.extend(timeline)
        for api_status in api_statuses:
            tweets[api_status.id] = {'text': api_status.text, 
            'user':api_status.user.id }
        return tweets

    @staticmethod
    def ExtractRatings(train_data, rating_set):
        """Extract rating matrix from a rating set based off training set"""
        tweets = CommonData.ExtractTweets(train_data)
        tweet_ids = sorted(tweets.keys())
        users = sorted(rating_set.keys())
        num_tweets = len(tweet_ids)
        num_users = len(users)    
        ratings_matrix = np.zeros((num_users, num_tweets))
        for i in range(num_users):
            rating_dict = rating_set[users[i]]
            for j in range(num_tweets):
                try: 
                    r = rating_dict[tweet_ids[j]].rating
                except KeyError:
                    r = 0
                ratings_matrix[i,j] = r
        return ratings_matrix
            
    @staticmethod
    def ExtractDictionary(train_data, d):
        """Extract a dictionary of all tokens keying to the tokens' frequencies 
        in frequency.
        """
        n_best = 200 #Number of best bigrams
        tweets = CommonData.ExtractTweets(train_data)
        frequency = collections.defaultdict(int)
        documents = []
        for tweet in tweets.values():
            words = ExtractTweetWords(tweet['text'], bigrams=False, d=d)
            documents.append(words)
            words.append("AUTHOR: {0}".format(tweet['user']))
            for w in words:
                if w: frequency[w] += 1
        bigram_finder = BigramCollocationFinder.from_documents(documents)    
        bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, n_best)
        for w in bigrams:
            if w: frequency[w] += 1
        return frequency

def repopulate(d):
    print d.rating_data

    for i in range(len(d.raters)):
        user_ratings = d.rating_data[d.raters[i]]
        rating_ids = user_ratings.keys()
        for rating_id in rating_ids:
            rating = d.rating_data[d.raters[i]][rating_id]
            rating.save()


class MultinomialBayesClassifier():
    """Defines a multinomial bayes classifier. This classifier can be be trained
    multiple times via the train function. Use predict to make new predictions
    on inputs. 
    """
    def __init__(self, d):
        """Corpus as a word -> index dict. Labels as label -> index dict"""
        self.corpus = d.corpus
        self.num_tokens = d.num_tokens
        self.corpus_lookup = d.corpus_lookup
        self.labels = d.labels
        self.num_labels = d.num_labels  
        self.labels_lookup = d.labels_lookup
        self.counts_y = np.zeros(self.num_labels)
        self.m = np.uint32(0)
        self.counts = np.zeros((self.num_labels, self.num_tokens))
        self.totals = np.zeros(self.num_labels)
        self.modified = 1        
        
    def train(self, feats):
        """Train a classifer with feats, can be trained more"""
        self.modified += 1        
        for token, label in feats:
            i = self.labels[label]
            try: j = self.corpus[token]
            except KeyError: continue
            self.counts[i, j] += 1
            self.totals[i] += 1
            self.counts_y[i] += 1
            self.m += 1
        
            
    def _freeze(self):
        """Freeze the classifier in a state to increase performance"""
        self.log_phi_y = np.log(self.counts_y/self.m)
        self.log_phi_x_y = np.log(np.transpose(np.divide(
            np.transpose(self.counts + 1), self.totals + self.num_tokens)))
        self.modified = 0            
            
    def predict(self, feats):
        """Predict feats using the classifier"""
        if self.modified > 0: self._freeze()
        log_proba = self.log_phi_y.copy()
        for token in feats:
            try: t = self.corpus[token]
            except KeyError: continue
            log_proba += self.log_phi_x_y[:, t]
        return self.labels_lookup[np.argmax(log_proba)]
        
    def show_most_informative_features(self, num_features=20):
        phi_y = np.transpose(np.divide(np.transpose(self.counts 
                                + 1), self.totals + self.num_tokens))
        best_labels = np.argmax(phi_y, axis=0)
        worst_labels = np.argmin(phi_y, axis=0)
        indicator = np.log(np.divide(np.amax(phi_y, axis=0),
                                  np.amin(phi_y, axis=0)))
        indicator = np.divide(np.amax(phi_y, axis=0), np.amin(phi_y, axis=0))
        best_indices = indicator.argsort()[-num_features:][::-1]
        print "Most Informative Features"        
        for i in best_indices:
            try:
                print "{0}\t {1} : {2} = {3}".format(self.corpus_lookup[i],
                    self.labels_lookup[best_labels[i]],
                    self.labels_lookup[worst_labels[i]],
                    indicator[i])
            except UnicodeEncodeError:
                print "Unprintable unicode token"
                
    def __add__(self, other):
        result = copy.copy(self)
        result.counts_y = np.add(self.counts_y, other.counts_y)
        result.m = np.add(self.m, other.m)
        result.counts = np.add(self.counts, other.counts)
        result.totals = np.add(self.totals, other.totals)
        return result
                
    def __iadd__(self, other):                
        self.counts_y = np.add(self.counts_y, other.counts_y)
        self.m = np.add(self.m, other.m)
        self.counts = np.add(self.counts, other.counts)
        self.totals = np.add(self.totals, other.totals)
        return self
        
    def __mul__(self, factor):
        result = copy.copy(self)
        result.counts_y = np.multiply(self.counts_y, factor)
        result.m = np.multiply(self.m, factor)
        result.counts = np.multiply(self.counts, factor)
        result.totals = np.multiply(self.totals, factor)
        return result
        
        
    __radd = __add__
    __rmul__ = __mul__         
            
class MultinomialCollatedClassifier(MultinomialBayesClassifier):
    def __init__(self, d, weights):
        MultinomialBayesClassifier.__init__(self, d)
        for id in weights:
            weight = weights[id]
            self += d.classifiers[id]*weight             
            
class TrainingStatistics(dict):
    """Subclasses dict so we can add / average statistics"""
    def __init__(self, d, classifications=None, labels=None):
        super(TrainingStatistics, self).__init__()
        self.labels = d.labels
        self.num_labels = d.num_labels
        self['tp'] = np.zeros(self.num_labels)
        self['fp'] = np.zeros(self.num_labels)
        self['fn'] = np.zeros(self.num_labels)
        self['tn'] = np.zeros(self.num_labels)
        if not classifications or not labels: return
        for c, y in zip(classifications, labels):
            for l in d.labels:
                # Does this work for arbitrarily many labels? Unsure...
                if c == y and c == l: self['tp'][self.labels[l]] += 1
                elif c != y and c == l: self['fp'][self.labels[l]] += 1
                elif c == y and c != l: self['tn'][self.labels[l]] += 1
                elif c != y and c != l: self['fn'][self.labels[l]] += 1        
        
    def __add__(self, other):
        result = copy.copy(self)
        for key in self.keys():
            result[key] = self[key] + other[key]
        return result
        
    def Precision(self, label):
        tp = self['tp'][self.labels[label]]
        fp = self['fp'][self.labels[label]]
        return tp / (tp + fp)
    
    def Recall(self, label):
        tp = self['tp'][self.labels[label]]
        fn = self['fn'][self.labels[label]]
        return tp / (tp + fn)
        
    def Accuracy(self, label):
        tp = self['tp'][self.labels[label]]
        fp = self['fp'][self.labels[label]]
        fn = self['fn'][self.labels[label]]
        tn = self['tn'][self.labels[label]]
        return (tp + tn) / (tp + tn + fp + fn)
        
    def __str__(self):
        s = "Training Statistics\n"
        for label in self.labels:
            s += "{0} precision: {1} \t recall: {2}\n".format(label,
            self.Precision(label), self.Recall(label))
        s += "accuracy: {0}\n\n".format(self.Accuracy(self.labels.keys()[0]))
        return s            
            
def ExtractWord(word, stemmer, d=None):
    """Extract a word to get rid of punctuation, stems words, and changes 
    links to the domain only. Returns None for stopwords.
    """
    def contains(string, query):
        return string.find(query) > -1
    word = word.strip(punctuation)
    if word.startswith(('http://', 'https://', 'www.')) or \
    contains(word, '.com') or contains(word, '.ly'):
        if contains(word, 'bit.ly'):
            return extract.grabDomain(word).lower()
            # Exceeded bit.ly api rate limit
            #return extract.grabDomain(extract.grabCanonicalUrl(word)).lower()
        return extract.grabDomain(word).lower()
    word = word.lower()
    if d:
        if word in d.stopwords:
            return None      
    else:
        if word in stopwords.words('english'):
            return None
    return stemmer.stem(word)

def ExtractTweetWords(text, bigrams=True, d=None):
    """Extract the tokens in a tweet based on ExtractWord"""
    stemmer = PorterStemmer()
    split_text = text.split()
    words = map(ExtractWord, split_text, [stemmer for _ in split_text], 
                [d for _ in split_text])
    words = [w for w in words if w]
    if bigrams == False:
        return words
    if bigrams == True: 
        bigram_finder = BigramCollocationFinder.from_words(words)    
        bigrams_tuple = bigram_finder.score_ngrams(BigramAssocMeasures.chi_sq)
        words.extend([bigram for bigram, score in bigrams_tuple])
        return words

def k_fold_cross_validation(X, K, randomise = False):
    """
    Generates K (training, validation) pairs from the items in X.
    
    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.
    
    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.
    """
    if randomise: from random import shuffle; X=list(X); shuffle(X)
    for k in xrange(K):
        training = [x for i, x in enumerate(X) if i % K != k]
        validation = [x for i, x in enumerate(X) if i % K == k]
        yield training, validation





def CreateTrainingSet(d, ids, ratings):
    """Create a set of labels + features suitable for in-house naive bayes 
    classifier
    """
    example_set = []
    for id in ids:
        words = ExtractTweetWords(d.tweets[id]['text'], bigrams=True, d=d)
        words.append("AUTHOR: {0}".format(d.tweets[id]['user']))
        rating = ratings[id].rating
        if rating == None: continue
        example_set.extend([(w, rating) for w in words])
    return example_set

def CreateTestSet(d, ids, ratings):
    example_set = []
    for id in ids:
        words = ExtractTweetWords(d.tweets[id]['text'], bigrams=True)
        words.append("AUTHOR: {0}".format(d.tweets[id]['user']))
        rating = ratings[id].rating
        if rating == None: continue
        example_set.append(((w for w in words), rating))
    return example_set



    

        
                                  
                                        
    
def ClassifyTest(d, weights, training, validation, ratings):
    """Train a collated multinomial classifer and test it on validation, 
    returning relevant statistics about the performance.
    """
    trainfeats = CreateTrainingSet(d, training, ratings)
    testfeats = CreateTestSet(d, validation, ratings)
    classifier = MultinomialCollatedClassifier(d, weights)    
    classifier.train(trainfeats)
    #classifier.show_most_informative_features(20)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set) 
    classifications = []
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.predict(feats)
        classifications.append(observed)
        testsets[observed].add(i)
    labels = [label for _, label in testfeats]
    stats = TrainingStatistics(d, classifications, labels)
    return stats

    

    
def FlatClusterFinder(linkage, target_num_clusters=None, target_cluster_size=None):
    """Find clusters of either cluster_size or num_clusters in linkage"""
    granularity = 1000.
    max_i = 4.0
    class FClusterList:
        def __init__(self, linkage):
            self.linkage = linkage
        def __getitem__(self, t):
            clusters = hierarchy.fcluster(linkage, t/granularity, 'distance')
            
            return -len(set(clusters))

    t = bisect.bisect(FClusterList(linkage), -target_num_clusters, 0, int(max_i*granularity))
    clusters = hierarchy.fcluster(linkage, t/granularity)
    print "t:" + str(t/granularity) + " clusters: " + str(clusters)
    return clusters

def IPythonImport():
    # Black magic to unpickle in ipython
    sys.modules['__main__'].TrainingSet = TrainingSet
    sys.modules['__main__'].TrainingUser = TrainingUser
    sys.modules['__main__'].CommonData = CommonData
    sys.modules['__main__'].MultinomialBayesClassifier = MultinomialBayesClassifier

def CophenetToWeight(distance):
    """Function to convert cophenet distance to weight"""
    return 1-distance ** 2

def CreateNLTKTweetSet(d, ids, ratings):
    """Create a set of labels + features suitable for nltk naive bayes 
    classifier
    """
    def get_feature(word):
        return dict([(word, 1.0)])
    example_set = []
    for id in ids:
        words = ExtractTweetWords(d.tweets[id]['text'], bigrams=True)
        words.append("AUTHOR: {0}".format(d.tweets[id]['user']))
        if ratings[id].rating == 1: rating = 1
        elif ratings[id].rating == -1: rating = -1
        else: continue
        example_set.extend([(get_feature(w), rating) for w in words])
    return example_set


def NaiveBayesNLTKClassifyTest(d, training, validation, ratings):
    """Train a naive bayes classifer and test it on validation, returning
    relevant statistics about the performance
    """
    trainfeats = CreateNLTKTweetSet(d, training, ratings)
    testfeats = CreateNLTKTweetSet(d, validation, ratings)
    classifier = NaiveBayesClassifier.train(trainfeats)
#    classifier.show_most_informative_features(50)        
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)        
    classifications = []
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        classifications.append(observed)
        testsets[observed].add(i)
    labels = [label for _, label in testfeats]
    stats = TrainingStatistics(d, classifications, labels)
    return stats
    '''
    stats = {}
    stats['like_precision'] = metrics.precision(refsets['like'], testsets['like'])
    stats['like_recall'] = metrics.recall(refsets['like'], testsets['like'])
    stats['dislike_precision'] = metrics.precision(refsets['dislike'], testsets['dislike'])
    stats['dislike_recall'] = metrics.recall(refsets['dislike'], testsets['dislike'])
    stats['accuracy'] = metrics.accuracy([label for _, label in testfeats], classifications)
    return stats
    '''

def main():
    IPythonImport()
    d = CommonData()    
    repopulate(d)
    return
    n_folds = 2
    random.seed()
    
    r_comp = pdist(d.ratings_matrix, 'jaccard')
    linkage = hierarchy.linkage(r_comp, method='average', metric='jaccard')
    cophenet = squareform(hierarchy.cophenet(linkage))
    hierarchy.dendrogram(linkage, color_threshold=-1)
    num_clusters = 16
    flat_clusters = FlatClusterFinder(linkage, num_clusters)
    
    total_stats = TrainingStatistics(d)
    for i in range(d.num_raters):
        user_ratings = d.rating_data[d.raters[i]]
        rating_ids = user_ratings.keys()
        if not rating_ids: continue
        rater_indices = np.where(flat_clusters == flat_clusters[i])[0]
        weights = {}
        for j in rater_indices:
            if j == i: continue
            distance = cophenet[i, j]
            weight = CophenetToWeight(distance)
            weights[j] = weight
        stats = TrainingStatistics(d)
        for training, validation in k_fold_cross_validation(
        rating_ids, K=n_folds, randomise = True):
            #stats += NaiveBayesNLTKClassifyTest(d, training, validation, user_ratings)
            stats += ClassifyTest(d, weights, training, validation, user_ratings)
        print "User {0}".format(d.raters[i])
        print stats
        total_stats += stats
    print total_stats
    



if __name__ == '__main__':
    #cProfile.runctx('main()', globals(), locals(), 'profile.txt')
    main()
