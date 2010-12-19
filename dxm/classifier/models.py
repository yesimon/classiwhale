from django.db import models
from picklefield.fields import PickledObjectField

class Classifier(models.Model):
    """Bug in scipy where dok_matrix cannot be pickled with cPickle 
    protocol 2 (default for picklefield)"""
    classifier = PickledObjectField()
    name = models.CharField(max_length=50)
    user_profile = models.ForeignKey('twitterauth.UserProfile')
    last_modified = models.DateTimeField(auto_now=True)


class TokenDictionary(models.Model):
    """
    Use id to index into array for classifiers using a
    sparse numpy array for faster performance. 
    """
    id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
