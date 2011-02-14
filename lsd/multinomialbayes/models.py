from django.db import models
from picklefield.fields import PickledObjectField

class MultinomialBayesModel(models.Model):
    """Bug in scipy where dok_matrix cannot be pickled with cPickle 
    protocol 2 (default for picklefield)"""
    data = PickledObjectField(compress=True)
    version = models.CharField(max_length=50)
    user_profile = models.ForeignKey('twitter.TwitterUserProfile')
    last_modified = models.DateTimeField(auto_now=True)


class TokenDictionary(models.Model):
    """
    Use id to index into array for classifiers using a
    sparse numpy array for faster performance. 
    """
    id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
