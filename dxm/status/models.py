from django.db import models

class Hashtag(models.Model):
    text = models.CharField(max_length=140, unique=True)
    
    def __unicode__(self):
        return self.text
    
class Hyperlink(models.Model):
    text = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return self.text
    
class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey('twitterauth.UserProfile')
    content_length = models.IntegerField()
    punctuation = models.IntegerField()
    has_hyperlink = models.BooleanField()
    hyperlinks = models.ManyToManyField(Hyperlink)
    hashtags = models.ManyToManyField(Hashtag)
    ats = models.ManyToManyField('twitterauth.UserProfile', related_name="status_ats")
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "statuses"
        
        
    @staticmethod
    def fullCreate(data):
        status = Status.objects.create(
                                        id = data['id'],
                                        text = data['text'],
                                        author = data['author'],
                                        has_hyperlink = data['has_hyperlink'],
                                        content_length = data['content_length'],
                                        punctuation = data['punctuation']
                                      )
        
        if 'hashtags' in data:
            for tag in data['hashtags']:
                ht, created = Hashtag.objects.get_or_create(text = tag)
                status.hashtags.add(ht)

        if 'hyperlinks' in data:
            for link in data['hyperlinks']:
                hl, created = Hyperlink.objects.get_or_create(text = link)
                status.hyperlinks.add(hl)

        if 'ats' in data:
            for name in data['ats']:
                user, created = UserProfile.objects.get_or_create(screen_name = name)
                status.ats.add(user)
        


    

