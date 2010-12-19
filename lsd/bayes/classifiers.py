# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import sys
# horrific path mangling here :(
sys.path.extend(['../../dxm/', '../', '../../lib/'])

# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)

################# Script #####################
import numpy as np
from scipy.sparse import dok_matrix, csc_matrix, lil_matrix

from extraction import SimpleExtractor
from classifier.models import Classifier, TokenDictionary
from twitterauth.models import UserProfile, Rating
from status.models import Status
import random
import collections
import copy 



class BayesCommonData():
    """ Elements in the dictionary 
    self.tokens
    self.labels
    self.tokens_lookup
    self.labels_lookup
    """
                

    labelings = (-1, 1)
    def __init__(self):
        self.update()

    def update(self):
        tokens = TokenDictionary.objects.all()
        self.tokens = {}
        self.tokens_lookup = {}
        for t in tokens:
            if not t.active: continue
            self.tokens[t.token] = t.id
            self.tokens_lookup[t.id] = t.token
        self.num_tokens = len(self.tokens)
        self.labels = {}
        self.labels_lookup = {}
        for i, label in enumerate(sorted(BayesCommonData.labelings)):
            self.labels[label] = i
            self.labels_lookup[i] = label
        self.num_labels = len(self.labels)





    def __str__(self):
        s = "Num tokens = {0} \nLabels: {1}".format(self.num_tokens,
                                            self.labels)
        return s




            
class MultinomialBayesClassifier(object):
    """Defines a multinomial bayes classifier. This classifier can be be trained
    multiple times via the train function. Use predict to make new predictions
    on inputs. 
    """
    def __init__(self, extractor=None, common=None):
        """Tokens as a word -> index dict. Labels as label -> index dict"""
        if extractor == None or common == None: raise UnboundLocalError
        self.update_common(common)
        self.extractor = extractor
        self.num_tokens = self.d.num_tokens
        self.num_labels = self.d.num_labels  
        self.counts_y = np.zeros((self.d.num_labels, 1))
        self.m = np.uint32(0)
        self.counts = lil_matrix((self.d.num_labels, self.d.num_tokens))
        self.totals = lil_matrix((self.d.num_tokens, 1))
        self.modified = 1    
        self.statuses = set()
        
    def update_common(self, common):
        setattr(self, 'd', common)
        
    def train(self, sr_tup):
        """Train a classifer with (status, rating) tuple, can be trained more"""
        d = self.d
        self.modified += 1
        status = sr_tup[0]
        if status.id in self.statuses or not status.text: return
        self.statuses.add(sr_tup[0].id)
        feats = [(t, sr_tup[1]) for t in self.extractor.ExtractStatus(sr_tup[0])]
        for token, label in feats:
            i = d.labels[label]
            try: j = d.tokens[token]
            except KeyError: continue
            self.counts[i, j] += 1
            self.totals[j, 0] += 1
            self.counts_y[i, 0] += 1
            self.m += 1
        
            
    def _freeze(self):
        """Freeze the classifier in a state to increase performance"""
        self.log_phi_y = np.log(self.counts_y/self.m)
        self.log_phi_x_y = csc_matrix(np.log(np.divide(
                         self.counts.todense() + 1, 
                         np.transpose(self.totals.todense()) + self.num_tokens)))
        self.modified = 0            
            
    def predict(self, status):
        """Predict status using the classifier, returns list"""
        d = self.d
        if self.modified > 0: self._freeze()
        log_proba = self.log_phi_y.copy()
        tokens = self.extractor.ExtractStatus(status)
        for token in tokens:
            try: t = d.tokens[token]
            except KeyError: continue
            log_proba += self.log_phi_x_y[:, t]
        return d.labels_lookup[np.argmax(log_proba)]
        
    def most_informative_features(self, num_features=20):
        d = self.d
        phi_y = np.divide(self.counts.todense() + 1, 
                   np.transpose(self.totals.todense()) + self.num_tokens)
        best_labels = np.argmax(phi_y, axis=0)
        worst_labels = np.argmin(phi_y, axis=0)
        indicator = np.log(np.divide(np.amax(phi_y, axis=0),
                                  np.amin(phi_y, axis=0)))
        indicator = np.divide(np.amax(phi_y, axis=0), np.amin(phi_y, axis=0))
        best_indices = indicator.argsort()[0, -num_features:]#[::-1]
        s = "Most Informative Features\n"        
        for n in range(num_features-1, 0, -1):
            i = best_indices[0, n]
            try:
                s += "{0}\t\t {1} : {2} = {3}\n".format(d.tokens_lookup[i],
                    d.labels_lookup[best_labels[0, i]],
                    d.labels_lookup[worst_labels[0, i]],
                    indicator[0, i])
            except UnicodeEncodeError:
                s += "Unprintable unicode token\n"
        return s
                
    def __add__(self, other):
        result = copy.copy(self)
        result.counts_y = np.add(self.counts_y, other.counts_y)
        result.m = np.add(self.m, other.m)
        result.counts = lil_matrix(np.add(self.counts.todense(),
                                          other.counts.todense()))
        result.totals = lil_matrix(np.add(self.totals.todense(), 
                                          other.totals.todense()))
        return result
                
    def __iadd__(self, other):                
        self.counts_y = np.add(self.counts_y, other.counts_y)
        self.m = np.add(self.m, other.m)
        self.counts = lil_matrix(np.add(self.counts.todense(),
                                        other.counts.todense()))
        self.totals = lil_matrix(np.add(self.totals.todense(),
                                        other.totals.todense()))
        return self
        
    def __mul__(self, factor):
        result = copy.copy(self)
        result.counts_y = np.multiply(self.counts_y, factor)
        result.m = np.multiply(self.m, factor)
        result.counts = lil_matrix(np.multiply(self.counts.todense(), factor))
        result.totals = lil_matrix(np.multiply(self.totals.todense(), factor))
        return result
        
        
    __radd = __add__
    __rmul__ = __mul__         


    def __getstate__(self):
        result = self.__dict__.copy()
        try: del result['d']
        except KeyError: pass
        return result

    @staticmethod        
    def test():
        d = BayesCommonData()
        c1 = MultinomialBayesClassifier(common=d, extractor=SimpleExtractor)
        c2 = MultinomialBayesClassifier(common=d, extractor=SimpleExtractor)
        superman = Status(id=1, text='superman')
        batman = Status(id=2, text='batman')
        spiderman = Status(id=3, text='spiderman')
        tset1 = [(superman, 1), (batman, -1)]
        tset2 = [(superman, -1), (spiderman, 1)]
        
        map(c1.train, tset1)
        map(c2.train, tset2)
        c3 = c1 + c2*2
        c3.update_common(d)
        print 'classifier 1: superman 1, batman -1'
        print 'superman predict: {0}'.format(c1.predict(superman))
        print 'batman predict: {0}'.format(c1.predict(batman))
        print
        print 'classifier 2: superman -1, spiderman 1'
        print 'superman predict: {0}'.format(c2.predict(superman))
        print 'batman predict: {0}'.format(c2.predict(batman))
        print
        print 'classifier 3: c1 + c2*2'
        print c3.most_informative_features()
        print 'superman predict: {0}'.format(c3.predict(superman))
        print 'batman predict: {0}'.format(c3.predict(batman))
        




class MultinomialCollatedClassifier(MultinomialBayesClassifier):
    def __init__(self, d, cwdict):
        MultinomialBayesClassifier.__init__(self, d)
        for classifier in cwdict:
            weight = cwdict[classifier]
            self += classifier*weight
            
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
            





    

if __name__ == '__main__':
    MultinomialBayesClassifier.test()
