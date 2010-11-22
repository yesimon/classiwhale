from django.db import models

class Hashtag(models.Model):
    text = models.CharField(max_length=140, unique=True)
    
    def __unicode__(self):
        return unicode(self.text)
    
class Hyperlink(models.Model):
    text = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return unicode(self.text)
    
class Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey('twitterauth.UserProfile', blank=True, null=True)
    content_length = models.IntegerField(blank=True, null=True)
    punctuation = models.IntegerField(blank=True, null=True)
    has_hyperlink = models.BooleanField(default=False)
    hyperlinks = models.ManyToManyField(Hyperlink, blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, null=True)
    ats = models.ManyToManyField('twitterauth.UserProfile', related_name="status_ats", blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.id)
    
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
        


    

