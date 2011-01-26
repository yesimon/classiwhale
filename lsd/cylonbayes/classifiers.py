######## Django Environment Setup #######

from django.core.management import setup_environ
import sys
# horrific path mangling here :(
sys.path.extend(['../../dxm/', '../', '../../lib/'])

# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)
    
######## Script Begin #######

import numpy as np
from scipy.sparse import dok_matrix, csc_matrix, lil_matrix

from twitterauth.models import UserProfile, Rating
from status.models import Status
from twitter import User
from algorithmio.classifier import Classifier
from django.core.cache import cache
from cylonbayes.models import *
from cylonbayes.extraction import BaltarExtractor
from django.core.exceptions import MultipleObjectsReturned
from operator import itemgetter
import collections
import copy 
import random
from math import exp


class CylonBayesData(object):
    labelings = (-1, 1)
    labels = {}
    labels_lookup = {}
    num_labels = 0
    for i, label in enumerate(sorted(labelings)):
        labels[label] = i
        labels_lookup[i] = label
        num_labels +=1

    def __init__(self, extractor=None):
        """Tokens as a word -> index dict. Labels as label -> index dict"""
        if extractor == None: raise UnboundLocalError
        self.extractor = extractor
        self.counts_y = np.zeros((self.num_labels, 1))
        self.m = np.uint32(0)
        self.counts = {}
        self.totals = {}
        self.modified = 1    
        self.statuses = set()
        
        
    def train(self, sr_tup):
        """Train a classifer with (status, rating) tuple, can be trained more"""
        self.modified += 1
        status = sr_tup[0]
        try: 
            if status.id in self.statuses or not status.text or not status.user: return
        except AttributeError: return
        self.statuses.add(sr_tup[0].id)
        try: i = self.labels[sr_tup[1]]
        except KeyError: raise
        feats = [(t, i) for t in self.extractor.ExtractStatus(sr_tup[0])]
        self.counts_y[i, 0] += 1
        for token, i in feats:
            if token not in self.totals:
                self.counts[token] = np.zeros((self.num_labels, 1))
                self.totals[token] = 0
            self.counts[token][i, 0] += 1
            self.totals[token] += 1
            self.m += 1                
            
    def _freeze(self):
        """Freeze the classifier in a state to increase performance"""
        self.log_phi_y = np.log(self.counts_y/len(self.statuses))
        self.log_phi_x_y = {}
        for token, counts in self.counts.iteritems():
            self.log_phi_x_y[token] = np.log(np.divide(counts + 1,
                             self.totals[token] + len(self.totals)))
        self.modified = 0            
            
    def predict(self, status):
        """Predict status using the classifier, returns list"""
        if self.modified > 0: self._freeze()
        log_proba = self.log_phi_y.copy()
        tokens = self.extractor.ExtractStatus(status)
        for token in tokens:
            try: 
                log_proba += self.log_phi_x_y[token][:]
            except KeyError: continue
        return log_proba

    def most_informative_features(self, num_features=20):
        phi_y = {}
        most_info = []
        for token, counts in self.totals.iteritems():
            phi_y[token] = np.divide(self.counts[token] + 1,
                                     self.totals[token] + len(self.totals))
            indicator = np.divide(np.amax(phi_y[token], axis=0), 
                                  np.amin(phi_y[token], axis=0))[0]
            most_info.append((token, indicator))
        most_info = sorted(most_info, key=lambda x: x[1], reverse=True)[:num_features]
        s = "Most Informative Features\n"        
        for token, indicator in most_info:
            try:
                s += "{0}\t\t {1} : {2} = {3}\n".format(token,
                    self.labels_lookup[np.argmax(phi_y[token], axis=0)[0]],
                    self.labels_lookup[np.argmin(phi_y[token], axis=0)[0]],
                    indicator)
            except UnicodeEncodeError:
                s += "Unprintable unicode token\n"
        return s            
                
    def __add__(self, other):
        result = copy.copy(self)
        result.counts_y = np.add(self.counts_y, other.counts_y)
        result.m = np.add(self.m, other.m)
        result.counts = copy.copy(self.counts)
        result.totals = copy.copy(self.totals)
        for token, counts in other.counts.iteritems():
            try: result.counts[token] = np.add(result.counts[token], counts)
            except KeyError: result.counts[token] = counts
        for token, totals in other.totals.iteritems():
            try: result.totals[token] = np.add(result.totals[token], totals)
            except KeyError: result.totals[token] = totals
        return result
                
    def __iadd__(self, other):                
        self.counts_y = np.add(self.counts_y, other.counts_y)
        self.m = np.add(self.m, other.m)
        for token, counts in other.counts.iteritems():
            try: self.counts[token] = np.add(self.counts[token], counts)
            except KeyError: self.counts[token] = counts
        for token, totals in other.totals.iteritems():
            try: self.totals[token] = np.add(self.totals[token], totals)
            except KeyError: self.totals[token] = totals
        return self
        
    def __mul__(self, factor):
        result = copy.copy(self)
        result.counts_y = np.multiply(self.counts_y, factor)
        result.m = np.multiply(self.m, factor)
        for token in self.counts.iterkeys():
            result.counts[token] = np.multiply(self.counts[token], factor)
            result.totals[token] = np.multiply(self.totals[token], factor)
        return result
        
        
    __radd = __add__
    __rmul__ = __mul__         

        





            
class CylonBayesClassifier(Classifier):
    """Defines a multinomial bayes classifier. This classifier can be be trained
    multiple times via the train function. Use predict to make new predictions
    on inputs.
    Contains instance variable:
    self.prof 
    """
    def convert_rating(rating):
        if isinstance(rating.status, Status):
            u = User(id=rating.status.user_profile_id)
            setattr(rating.status, 'user', u)
        return rating

    def force_train(self):
        """Concrete method for Classifier"""
        mb_model = self.get_cylon_bayes_model()
        mb = mb_model.data
        seen_statuses = mb.statuses
        ratings_list = Rating.objects.filter(user_profile=self.prof).exclude(
            status__id__in=seen_statuses).order_by(
            '-rated_time').select_related('status')
        train_set = []
        for rating in ratings_list:
            convert_rating(rating)
            train_set.append((rating.status, rating.rating))
        map(mb.train, train_set)
        mb_model.save()

    def test_train(self, ratings=None, clicks=None):
        mb = CylonBayesData(extractor=BaltarExtractor)
        train_set = []
        for rating in ratings:
            convert_rating(rating)
            train_set.append((rating.status, rating.rating))
        map(mb.train, train_set)
        self.mb = mb
        return self

    def test_predict(self, statuses):
        return predict(self, statuses, test=True)

    def predict(self, statuses, test=False):
        """Concrete method for Classifier"""
        if test: mb = self.mb 
        else:
            mb_model = self.get_cylon_bayes_model()
            mb = mb_model.data
        log_probas = map(mb.predict, statuses)
        indexes = range(len(log_probas[0]))
        expects = [sorted([(mb.labels_lookup[i], log_proba[i, 0]) 
            for i in indexes], key=itemgetter(1), reverse=True)
            for log_proba in log_probas]
        a = map(self.renormalization, expects)
        return a

    def renormalization(self, expect):
        """Expect as a sorted list of (label, probability)"""
        conf = exp(expect[0][1]) / (exp(expect[0][1]) + exp(expect[1][1]))
#        print "e1: {0}, e2: {1}".format(expect[0][1], expect[1][1])
        if np.isnan(conf):
            return 1
        return conf*expect[0][0]

    def get_cylon_bayes_model(self):
        try:
            c_obj = CylonBayesModel.objects.get(user_profile=self.prof, version=self.prof.classifier_version)
        except CylonBayesModel.DoesNotExist:
            c = CylonBayesData(extractor=BaltarExtractor)
            c_obj = CylonBayesModel(user_profile=self.prof, data=c, version=self.prof.classifier_version)
        except MultipleObjectsReturned:
            # Should never happen to have two classifiers of same version
            c_objs = CylonBayesModel.objects.filter(version=self.prof.classifier_version)
            [c.delete for c in c_objs[1:]]
            c_obj = c_objs[0]
        return c_obj

    def round_away(num, split=0.0):
        if num >= split: return 1
        else: return -1

    def create_training_set():
        pass




    @staticmethod        
    def test():
        c1 = CylonBayesData(extractor=BaltarExtractor)
        c2 = CylonBayesData(extractor=BaltarExtractor)
        superman = Status(id=1, text='superman')
        batman = Status(id=2, text='batman')
        spiderman = Status(id=3, text='spiderman http://nyti.ms/gl8sjV')
        setattr(superman, 'user', User(id=42))
        setattr(batman, 'user', User(id=44))
        setattr(spiderman, 'user', User(id=43))


        tset1 = [(superman, 1), (batman, -1)]
        tset2 = [(superman, -1), (spiderman, 1)]
        
        map(c1.train, tset1)
        map(c2.train, tset2)
        c3 = c1 + c2*2
        print 'classifier 1: superman 1, batman -1'
        print 'superman predict: {0}'.format(c1.predict(superman))
        print 'batman predict: {0}'.format(c1.predict(batman))
        print
        print 'classifier 2: superman -1, spiderman 1'
        print 'superman predict: {0}'.format(c2.predict(superman))
        print 'batman predict: {0}'.format(c2.predict(batman))
        print 'spiderman predict: {0}'.format(c2.predict(spiderman))
        print
        print 'classifier 3: c1 + c2*2'
        print c3.most_informative_features()
        print 'superman predict: {0}'.format(c3.predict(superman))
        print 'batman predict: {0}'.format(c3.predict(batman))
        


class CylonCollatedClassifier(CylonBayesClassifier):
    def __init__(self, cwdict):
        CylonBayesClassifier.__init__(self)
        for classifier in cwdict:
            weight = cwdict[classifier]
            self += classifier*weight
            
class TrainingStatistics(dict):
    """Subclasses dict so we can add / average statistics"""
    def __init__(self, classifier, classifications=None, labels=None):
        super(TrainingStatistics, self).__init__()
        self.labels = classifier.labels
        self.num_labels = len(classifier.labels)
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
            

if __name__ == '__main__':
    CylonBayesClassifier.test()
