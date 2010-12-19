# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Hashtag'
        db.create_table('status_hashtag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=140)),
        ))
        db.send_create_signal('status', ['Hashtag'])

        # Adding model 'Hyperlink'
        db.create_table('status_hyperlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('status', ['Hyperlink'])

        # Adding model 'Status'
        db.create_table('status_status', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterauth.UserProfile'], null=True, blank=True)),
            ('content_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('punctuation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('has_hyperlink', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('in_reply_to_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_replies', null=True, to=orm['twitterauth.UserProfile'])),
            ('in_reply_to_status', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='status_replies', null=True, to=orm['status.Status'])),
        ))
        db.send_create_signal('status', ['Status'])

        # Adding M2M table for field hyperlinks on 'Status'
        db.create_table('status_status_hyperlinks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('status', models.ForeignKey(orm['status.status'], null=False)),
            ('hyperlink', models.ForeignKey(orm['status.hyperlink'], null=False))
        ))
        db.create_unique('status_status_hyperlinks', ['status_id', 'hyperlink_id'])

        # Adding M2M table for field hashtags on 'Status'
        db.create_table('status_status_hashtags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('status', models.ForeignKey(orm['status.status'], null=False)),
            ('hashtag', models.ForeignKey(orm['status.hashtag'], null=False))
        ))
        db.create_unique('status_status_hashtags', ['status_id', 'hashtag_id'])

        # Adding M2M table for field ats on 'Status'
        db.create_table('status_status_ats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('status', models.ForeignKey(orm['status.status'], null=False)),
            ('userprofile', models.ForeignKey(orm['twitterauth.userprofile'], null=False))
        ))
        db.create_unique('status_status_ats', ['status_id', 'userprofile_id'])


    def backwards(self, orm):
        
        # Deleting model 'Hashtag'
        db.delete_table('status_hashtag')

        # Deleting model 'Hyperlink'
        db.delete_table('status_hyperlink')

        # Deleting model 'Status'
        db.delete_table('status_status')

        # Removing M2M table for field hyperlinks on 'Status'
        db.delete_table('status_status_hyperlinks')

        # Removing M2M table for field hashtags on 'Status'
        db.delete_table('status_status_hashtags')

        # Removing M2M table for field ats on 'Status'
        db.delete_table('status_status_ats')


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
        'status.hashtag': {
            'Meta': {'object_name': 'Hashtag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '140'})
        },
        'status.hyperlink': {
            'Meta': {'object_name': 'Hyperlink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'status.status': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Status'},
            'ats': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'status_ats'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['twitterauth.UserProfile']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterauth.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'content_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'has_hyperlink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashtags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['status.Hashtag']", 'null': 'True', 'blank': 'True'}),
            'hyperlinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['status.Hyperlink']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'in_reply_to_status': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'status_replies'", 'null': 'True', 'to': "orm['status.Status']"}),
            'in_reply_to_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_replies'", 'null': 'True', 'to': "orm['twitterauth.UserProfile']"}),
            'punctuation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'twitterauth.rating': {
            'Meta': {'object_name': 'Rating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rated_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['status.Status']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterauth.UserProfile']"})
        },
        'twitterauth.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['status.Status']", 'symmetrical': 'False', 'through': "orm['twitterauth.Rating']", 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'training_statuses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['status.Status']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['status']