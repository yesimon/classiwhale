# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TwitterUserProfile'
        db.create_table('twitter_twitteruserprofile', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.UserProfile'])),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('oauth_secret', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('profile_image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('profile_use_background_image', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_sidebar_border_color', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('profile_background_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('profile_sidebar_fill_color', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('profile_background_image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('profile_background_color', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('profile_link_color', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('friends_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('followers_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('statuses_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('active_classifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('classifier_version', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('whale', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['whale.Whale'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('twitter', ['TwitterUserProfile'])

        # Adding M2M table for field training_statuses on 'TwitterUserProfile'
        db.create_table('twitter_twitteruserprofile_training_statuses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('twitteruserprofile', models.ForeignKey(orm['twitter.twitteruserprofile'], null=False)),
            ('status', models.ForeignKey(orm['twitter.status'], null=False))
        ))
        db.create_unique('twitter_twitteruserprofile_training_statuses', ['twitteruserprofile_id', 'status_id'])

        # Adding model 'Status'
        db.create_table('twitter_status', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitter.TwitterUserProfile'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('punctuation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('has_hyperlink', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('in_reply_to_user_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('in_reply_to_status_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('twitter', ['Status'])

        # Adding M2M table for field hyperlinks on 'Status'
        db.create_table('twitter_status_hyperlinks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('status', models.ForeignKey(orm['twitter.status'], null=False)),
            ('hyperlink', models.ForeignKey(orm['twitter.hyperlink'], null=False))
        ))
        db.create_unique('twitter_status_hyperlinks', ['status_id', 'hyperlink_id'])

        # Adding M2M table for field hashtags on 'Status'
        db.create_table('twitter_status_hashtags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('status', models.ForeignKey(orm['twitter.status'], null=False)),
            ('hashtag', models.ForeignKey(orm['twitter.hashtag'], null=False))
        ))
        db.create_unique('twitter_status_hashtags', ['status_id', 'hashtag_id'])

        # Adding M2M table for field ats on 'Status'
        db.create_table('twitter_status_ats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('status', models.ForeignKey(orm['twitter.status'], null=False)),
            ('twitteruserprofile', models.ForeignKey(orm['twitter.twitteruserprofile'], null=False))
        ))
        db.create_unique('twitter_status_ats', ['status_id', 'twitteruserprofile_id'])

        # Adding model 'Rating'
        db.create_table('twitter_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitter.TwitterUserProfile'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitter.Status'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rated_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('twitter', ['Rating'])

        # Adding model 'Hashtag'
        db.create_table('twitter_hashtag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=140)),
        ))
        db.send_create_signal('twitter', ['Hashtag'])

        # Adding model 'Hyperlink'
        db.create_table('twitter_hyperlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('twitter', ['Hyperlink'])


    def backwards(self, orm):
        
        # Deleting model 'TwitterUserProfile'
        db.delete_table('twitter_twitteruserprofile')

        # Removing M2M table for field training_statuses on 'TwitterUserProfile'
        db.delete_table('twitter_twitteruserprofile_training_statuses')

        # Deleting model 'Status'
        db.delete_table('twitter_status')

        # Removing M2M table for field hyperlinks on 'Status'
        db.delete_table('twitter_status_hyperlinks')

        # Removing M2M table for field hashtags on 'Status'
        db.delete_table('twitter_status_hashtags')

        # Removing M2M table for field ats on 'Status'
        db.delete_table('twitter_status_ats')

        # Deleting model 'Rating'
        db.delete_table('twitter_rating')

        # Deleting model 'Hashtag'
        db.delete_table('twitter_hashtag')

        # Deleting model 'Hyperlink'
        db.delete_table('twitter_hyperlink')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'whale': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['whale.Whale']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "['-rated_time']", 'object_name': 'Rating'},
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
            'place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'punctuation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitter.TwitterUserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'twitter.twitteruserprofile': {
            'Meta': {'object_name': 'TwitterUserProfile'},
            'active_classifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'classifier_version': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'friends_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profile.UserProfile']"}),
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

    complete_apps = ['twitter']
