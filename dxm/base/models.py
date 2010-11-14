from django.db import models

# Create your models here.


class Hashtag(models.Model):
	text = models.CharField(max_length=140, unique=1)
	