# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'StreamDiff'
        db.create_table('algorithmio_streamdiff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterauth.UserProfile'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['status.Status'])),
            ('diff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('score', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=8)),
            ('algorithm', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('filter_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('algorithmio', ['StreamDiff'])


    def backwards(self, orm):
        
        # Deleting model 'StreamDiff'
        db.delete_table('algorithmio_streamdiff')


    models = {
        'algorithmio.streamdiff': {
            'Meta': {'object_name': 'StreamDiff'},
            'algorithm': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'diff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '8'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['status.Status']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterauth.UserProfile']"})
        },
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
        'classifier.classifier': {
            'Meta': {'object_name': 'Classifier'},
            'classifier': ('picklefield.fields.PickledObjectField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterauth.UserProfile']"})
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'active_classifier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'active_classifier'", 'null': 'True', 'to': "orm['classifier.Classifier']"}),
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

    complete_apps = ['algorithmio']
