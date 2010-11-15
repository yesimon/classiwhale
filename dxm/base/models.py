from django.db import models
from twitterauth.models import UserProfile


class Hashtag(models.Model):
	text = models.CharField(max_length=140, unique=1)
	
	def __unicode__(self):
		return self.text
	
	
	
class Hyperlink(models.Model):
	text = models.CharField(max_length=255, unique=1)
	
	def __unicode__(self):
		return self.text
	



class Tweet(models.Model):
	author = models.IntegerField()
	content_length = models.IntegerField()
	punctuation = models.IntegerField()
	has_hyperlink = models.BooleanField()
	hyperlinks = models.ManyToManyField(Hyperlink)
	hashtags = models.ManyToManyField(Hashtag)
	ats = models.ManyToManyField(UserProfile)
	
	@staticmethod
	def fullCreate(data):
		twt = Tweet.objects.create(
                                    author = data['author'],
                                    has_hyperlink = data['has_hyperlink'],
                                    content_length = data['content_length'],
                                    punctuation = data['punctuation']
                                    )
		twt.save()
        
		if 'hashtags' in data:
			for tag in data['hashtags']:
				ht, created = Hashtag.objects.get_or_create(text = tag)
				twt.hashtags.add(ht)

		if 'hyperlinks' in data:
			for link in data['hyperlinks']:
				hl, created = Hyperlink.objects.get_or_create(text = link)
				twt.hyperlinks.add(hl)

		if 'ats' in data:
			for name in data['ats']:
				user, created = UserProfile.objects.get_or_create(screen_name = name)
				twt.ats.add(user)


	
	

class Rating(models.Model):
	user = models.ForeignKey(UserProfile)
	tweet = models.ForeignKey(Tweet)
	rating = models.IntegerField()
	

	
	

