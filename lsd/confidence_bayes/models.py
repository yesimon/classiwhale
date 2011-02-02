from django.db import models
from picklefield.fields import PickledObjectField



class pUAFgR_Model(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey('twitterauth.UserProfile')
    author_id = models.ForeignKey('twitterauth.UserProfile', related_name='author_id')
    token_id = models.IntegerField() # the features F
    probability = models.FloatField()
    samples = models.IntegerField()