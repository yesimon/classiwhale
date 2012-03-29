from django.db import models
from picklefield.fields import PickledObjectField

class CylonBayesModel(models.Model):
    """Bug in scipy where dok_matrix cannot be pickled with cPickle 
    protocol 2 (default for picklefield)"""
    data = PickledObjectField(compress=True)
    version = models.CharField(max_length=50)
    user_profile = models.ForeignKey('twitter.TwitterUserProfile')
    last_modified = models.DateTimeField(auto_now=True)


