
from django.core.management import setup_environ
import sys
# horrific path mangling here :(
sys.path.extend(['../../dxm/', '../', '../../lib/'])

# For production use
# sys.path.append('/var/www/classiwhale/dxm/')

import settings
setup_environ(settings)
    


# -*- coding: utf-8 -*-
import numpy as np
from scipy.sparse import dok_matrix, csc_matrix, lil_matrix

from extraction import SimpleExtractor
from algorithmio.classifier import Classifier
from django.core.cache import cache
from classifiers.models import *
from django.core.exceptions import MultipleObjectsReturned
from operator import itemgetter
import collections
import copy 

from twitter.models import TwitterUserProfile, Rating, Status



            
class ConfidenceBayes(Classifier):
    """
    The following convention is used here:
    R = rating {-1, 1}
    U = active_user
    A = the author of the tweet being classified
    F = tweet features, including words and metadata
    
    In function names, pUFgR means P(U,F | R)
    confidence['UFgR'] corresponds to the confidence (i.e. # of samples) for P(U,F | R)
    """
    
    THRESHOLD = 10  # when the number of samples for a probability exceeds
                               # this value, the probability will not be factored
    

    """
    The following methods assume that all probabilities are precomputed and cached.
    """
    def get_pRUAF(self):
        return get_pR() * get_pUAFgR();
    
    # independent of user
    def get_pR(self):
        return 0.5

    def get_pUAFgR(self):
        if confidence['UAFgR'] >= ConfidenceBayes.THRESHOLD:
            return 1



    def force_train(self):
        """Concrete method for Classifier"""
        

    def predict(self, statuses):
        """Concrete method for Classifier"""     


