from __future__ import division
from django.db import models
from django.core import serializers
from django.db import transaction, connection
from picklefield.fields import PickledObjectField
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate
from time import mktime
import json

from profile.models import UserProfile
from twitter.managers import (TwitterUserProfileManager, StatusManager, 
                              CachedStatusManager )


JSON_COMPACT = (',',':')

class TwitterUserProfile(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    oauth_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    oauth_secret = models.CharField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    screen_name = models.CharField(max_length=32, blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    profile_use_background_image = models.BooleanField(default=False)
    profile_sidebar_border_color = models.CharField(max_length=16, blank=True, null=True)
    profile_background_title = models.CharField(max_length=255, blank=True, null=True)
    profile_sidebar_fill_color = models.CharField(max_length=16, blank=True, null=True)
    profile_background_image_url = models.URLField(blank=True, null=True)
    profile_background_color = models.CharField(max_length=16, blank=True, null=True)
    profile_link_color = models.CharField(max_length=16, blank=True, null=True)
    utc_offset = models.IntegerField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    location = models.CharField(max_length=160, blank=True, null=True)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    friends_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0)
    description = models.CharField(max_length=160, blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)
    ratings = models.ManyToManyField('Status', blank=True, through='Rating')
    training_statuses = models.ManyToManyField('Status', blank=True, null=True, related_name='training')
    active_classifier = models.CharField(max_length=50, blank=True, null=True)
    classifier_version = models.CharField(max_length=30, blank=True, null=True)
    whale = models.OneToOneField('whale.Whale', blank=True, null=True)
    cached_statuses = models.ManyToManyField('Status', blank=True, null=True, through='CachedStatus', related_name='cached_statuses')
    cached_time = models.DateTimeField(blank=True, null=True)
    cached_maxid = models.BigIntegerField(blank=True, null=True)
    cached_minid = models.BigIntegerField(blank=True, null=True)
    available_fields = ('id', 'name', 'screen_name', 'profile_image_url', 
                        'profile_use_background_image', 
                        'profile_sidebar_border_color', 
                        'profile_sidebar_fill_color', 
                        'profile_background_image_url', 
                        'profile_background_color', 
                        'profile_link_color', 
                        'verified', 'protected', 'location', 'url', 
                        'friends_count', 'followers_count', 'statuses_count', 
                        'description', 'utc_offset')
    internal_fields = ('user', 'oauth_token', 'oauth_secret',
                       'active_classifier', 'classifier_version', 'whale', 
                       'cached_time')

    objects = TwitterUserProfileManager()

    def __unicode__(self):
        return "%s's twitter profile" % self.screen_name

    @staticmethod
    def savemany(tps, *args, **kwargs):
        found_tps = set(TwitterUserProfile.objects.in_bulk([tp.id for tp in tps]).keys())
        for tp in tps:
            if tp.id in found_tps: continue
            found_tps.add(tp.id)
            tp.save(force_insert=True, *args, **kwargs)




    def as_json_string(self):
        json_dict = self.deconstruct_to_dict()
        try: json_string = json.dumps(json_dict, separators=JSON_COMPACT)
        except: pass
        return json_string

    @classmethod
    def construct_from_dict(cls, data):
        field_dict = {}
        for key, value in data.iteritems():
            if key in cls.available_fields:
                field_dict[str(key)] = value       
        user = cls(**field_dict)
        return user

    @staticmethod
    def construct_from_dicts(dicts):
        return map(TwitterUserProfile.construct_from_dict, dicts)


    def deconstruct_to_dict(self):
        data = {}
        for field in self.available_fields:
            data[field] = getattr(self, field) 
        return data

    


class Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey('TwitterUserProfile', blank=True, null=True)
#    place = PickledObjectField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    content_length = models.IntegerField(blank=True, null=True)
    punctuation = models.IntegerField(blank=True, null=True)
    has_hyperlink = models.BooleanField(default=False)
    hyperlinks = models.ManyToManyField('Hyperlink', blank=True, null=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True, null=True)
    ats = models.ManyToManyField('TwitterUserProfile', related_name="status_ats", blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    in_reply_to_user_id = models.IntegerField(blank=True, null=True)
    in_reply_to_status_id = models.BigIntegerField(blank=True, null=True)
    is_cached = models.BooleanField(default=False) # False for permanent store

    objects = StatusManager()

    available_fields = ('id', 'text', 'user',  'source', 'created_at',
                        'in_reply_to_user_id', 'in_reply_to_status_id')

    internal_fields = ('is_cached', 'user_id' )

    """
    # Override=True uses normal save
    def save(self, override=False, *args, **kwargs):
        if override: 
            status = self
        else:
            field_dict = {}
            for key, value in self.__dict__.iteritems():
                if key in self.available_fields or key in self.internal_fields:
                    field_dict[str(key)] = value
            status = Status(**field_dict)
        super(Status, status).save(*args, **kwargs)
    """

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "statuses"

    def __unicode__(self):
        return unicode(self.id)

    def save_with_user(self, is_cached=False):
        try: TwitterUserProfile.objects.get(id=self.user.id)
        except TwitterUserProfile.DoesNotExist:
            self.user.save()
        try: 
            Status.objects.get(id=self.id)
            return
        except Status.DoesNotExist: pass
        self.is_cached = is_cached
        self.save()

    @staticmethod
    def savemany(statuses, is_cached=False):
        tps = [s.user for s in statuses]
        TwitterUserProfile.savemany(tps)
        s_found = set(Status.objects.in_bulk([s.id for s in statuses]).keys())
        to_save = []
        for s in statuses:
            if s.id in s_found: continue
            s_found.add(s.id)
            s.is_cached = is_cached
            to_save.append(s)
        Status.objects.create_in_bulk(to_save)

    # Consider delete by ids if filtering is_cached takes a long time
    @staticmethod
    def clear_cache(max_id=None, td=timedelta(hours=72)):
        if max_id:
            statuses = Status.objects.filter(is_cached=True).filter(id__lt=max_id)
        else:
            now = datetime.utcnow()
            statuses = Status.objects.filter(is_cached=True).filter(
                                      created_at__lt=now-td)
        details = CachedStatus.objects.filter(status__is_cached=False).filter(
                                      status__created_at__lt=now-td)
        statuses.delete()
        details.delete()



    @classmethod
    def construct_from_dict(cls, data):
        if 'user' not in data:
            raise KeyError
        data['user'] = TwitterUserProfile.construct_from_dict(data['user'])
        data['created_at'] = datetime.fromtimestamp(mktime(parsedate(data['created_at'])))
        field_dict = {}
        for key, value in data.iteritems():
            if key in cls.available_fields:
                field_dict[str(key)] = value
        status = Status(**field_dict)
        return status

    @classmethod
    def construct_from_search_dict(cls, data):
        if 'metadata' not in data:
            raise KeyError
        data['created_at'] = datetime.fromtimestamp(mktime(parsedate(data['created_at'])))
        user = TwitterUserProfile(profile_image_url=data['profile_image_url'],
                                  screen_name=data['from_user'])
        data['user'] = user
        field_dict = {}
        for key, value in data.iteritems():
            if key in cls.available_fields:
                field_dict[str(key)] = value
        status = Status(**field_dict)
        return status

    def deconstruct_to_dict(self):
        data = {}
        for field in self.available_fields:
            data[field] = getattr(self, field) 
        data['user'] = TwitterUserProfile.deconstruct_to_dict(self.user)
        data['created_at'] = formatdate(timeval=mktime(self.created_at.timetuple()),
                                        localtime=False, usegmt=True)
        return data

    def as_json_string(self):
        json_dict = self.deconstruct_to_dict()
        json_string = json.dumps(json_dict, separators=JSON_COMPACT)
        return json_string

    @staticmethod
    def construct_from_dicts(dicts):
        return map(Status.construct_from_dict, dicts)

    @staticmethod
    def construct_from_search_dicts(dicts):
        return map(Status.construct_from_search_dict, dicts)

    def relative_created_at(self):
        '''Get a human redable string representing the posting time

        Returns:
          A human readable string representing the posting time
        '''
        fudge = 1.25
        td  = datetime.utcnow() - self.created_at
        delta = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

        if delta < (1 * fudge):
          return 'about a second ago'
        elif delta < (60 * (1/fudge)):
          return 'about %d seconds ago' % (delta)
        elif delta < (60 * fudge):
          return 'about a minute ago'
        elif delta < (60 * 60 * (1/fudge)):
          return 'about %d minutes ago' % (delta / 60)
        elif delta < (60 * 60 * fudge) or delta / (60 * 60) == 1:
          return 'about an hour ago'
        elif delta < (60 * 60 * 24 * (1/fudge)):
          return 'about %d hours ago' % (delta / (60 * 60))
        elif delta < (60 * 60 * 24 * fudge) or delta / (60 * 60 * 24) == 1:
          return 'about a day ago'
        else:
          return 'about %d days ago' % (delta / (60 * 60 * 24))        

    @staticmethod
    def fullCreate(data):
        """Create status from dictionary"""
        status = Status.objects.create(
                                id = data['id'],
                                text = data['text'],
                                user = data['user'],
                                place = data['place'],
                                source = data['source'],
                                in_reply_to_user_id = data['in_reply_to_user_id'],
                                in_reply_to_status_id = data['in_reply_to_status_id'],
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




class CachedStatus(models.Model):
    user = models.ForeignKey('TwitterUserProfile')
    status = models.ForeignKey('Status')
    prediction = models.FloatField(blank=True, null=True)
    class Meta:
        unique_together = ('user', 'status')
        ordering = ['status']
    objects = CachedStatusManager()


class Rating(models.Model):
    user = models.ForeignKey('TwitterUserProfile') 
    status = models.ForeignKey('Status') 
    rating = models.IntegerField(blank=True, null=True)
    rated_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Ratings"
        get_latest_by = "rated_time"
        ordering = ['-rated_time']
        unique_together = ("user", "status")

    @staticmethod
    def appendTo(statuses, prof):
        ratings = Rating.objects.filter(user=prof.id,
                                        status__in=[s.id for s in statuses])
        rd = dict([(r.status_id, r) for r in ratings])
        for s in statuses:
            try:
                r = rd[s.id]
                s.rating = r.rating
                if r.rating == 1:
                    s.likeClass = ' active'
                    s.dislikeClass = ' inactive'
                if r.rating == -1:
                    s.likeClass = ' inactive'
                    s.dislikeClass = ' active'
            except KeyError:
                continue

class Hashtag(models.Model):
    text = models.CharField(max_length=140, unique=True)
    
    def __unicode__(self):
        return unicode(self.text)
    
    
class Hyperlink(models.Model):
    text = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return unicode(self.text)

