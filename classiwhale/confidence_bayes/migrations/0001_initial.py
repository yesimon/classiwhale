# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'pUAFgR_Model'
        db.create_table('confidence_bayes_puafgr_model', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitter.TwitterUserProfile'])),
            ('author_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author_id', to=orm['twitter.TwitterUserProfile'])),
            ('token_id', self.gf('django.db.models.fields.IntegerField')()),
            ('probability', self.gf('django.db.models.fields.FloatField')()),
            ('samples', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('confidence_bayes', ['pUAFgR_Model'])

    def backwards(self, orm):
        # Deleting model 'pUAFgR_Model'
        db.delete_table('confidence_bayes_puafgr_model')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'confidence_bayes.puafgr_model': {
            'Meta': {'object_name': 'pUAFgR_Model'},
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author_id'", 'to': "orm['twitter.TwitterUserProfile']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'probability': ('django.db.models.fields.FloatField', [], {}),
            'samples': ('django.db.models.fields.IntegerField', [], {}),
            'token_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.TwitterUserProfile']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'whale': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whale.Whale']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'twitter.cachedstatus': {
            'Meta': {'ordering': "['status']", 'unique_together': "(('user', 'status'),)", 'object_name': 'CachedStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prediction': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.Status']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.TwitterUserProfile']"})
        },
        'twitter.hashtag': {
            'Meta': {'object_name': 'Hashtag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '140'})
        },
        'twitter.hyperlink': {
            'Meta': {'object_name': 'Hyperlink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'twitter.rating': {
            'Meta': {'ordering': "['-rated_time']", 'unique_together': "(('user', 'status'),)", 'object_name': 'Rating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rated_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.Status']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.TwitterUserProfile']"})
        },
        'twitter.status': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Status'},
            'ats': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'status_ats'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['twitter.TwitterUserProfile']"}),
            'content_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_hyperlink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashtags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['twitter.Hashtag']", 'null': 'True', 'blank': 'True'}),
            'hyperlinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['twitter.Hyperlink']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'in_reply_to_status_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'in_reply_to_user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_cached': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'punctuation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.TwitterUserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'twitter.twitteruserprofile': {
            'Meta': {'object_name': 'TwitterUserProfile'},
            'active_classifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cached_maxid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cached_minid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cached_statuses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cached_statuses'", 'to': "orm['twitter.Status']", 'through': "orm['twitter.CachedStatus']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'cached_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'classifier_version': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'friends_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profile_background_color': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'profile_background_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile_background_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile_link_color': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'profile_sidebar_border_color': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'profile_sidebar_fill_color': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'profile_use_background_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['twitter.Status']", 'symmetrical': 'False', 'through': "orm['twitter.Rating']", 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'statuses_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'training_statuses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['twitter.Status']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profile.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'utc_offset': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'whale': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whale.Whale']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'whale.whale': {
            'Meta': {'object_name': 'Whale'},
            'exp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'My Whale'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['whale.WhaleSpecies']", 'null': 'True', 'blank': 'True'})
        },
        'whale.whalespecies': {
            'Meta': {'object_name': 'WhaleSpecies'},
            'evolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whale.WhaleSpecies']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'minExp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Baby Whale'", 'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['confidence_bayes']