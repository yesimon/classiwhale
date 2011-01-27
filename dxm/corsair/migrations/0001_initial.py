# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TrainingSet'
        db.create_table('corsair_trainingset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('corsair', ['TrainingSet'])

        # Adding M2M table for field user_profiles on 'TrainingSet'
        db.create_table('corsair_trainingset_user_profiles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trainingset', models.ForeignKey(orm['corsair.trainingset'], null=False)),
            ('userprofile', models.ForeignKey(orm['twitterauth.userprofile'], null=False))
        ))
        db.create_unique('corsair_trainingset_user_profiles', ['trainingset_id', 'userprofile_id'])

        # Adding M2M table for field ratings on 'TrainingSet'
        db.create_table('corsair_trainingset_ratings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trainingset', models.ForeignKey(orm['corsair.trainingset'], null=False)),
            ('rating', models.ForeignKey(orm['twitterauth.rating'], null=False))
        ))
        db.create_unique('corsair_trainingset_ratings', ['trainingset_id', 'rating_id'])

        # Adding model 'PredictionStatistics'
        db.create_table('corsair_predictionstatistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('training_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['corsair.TrainingSet'])),
            ('classifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('raw_data', self.gf('picklefield.fields.PickledObjectField')()),
            ('discrimination_bound', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('n_folds', self.gf('django.db.models.fields.IntegerField')()),
            ('ppv', self.gf('django.db.models.fields.FloatField')()),
            ('npv', self.gf('django.db.models.fields.FloatField')()),
            ('tpr', self.gf('django.db.models.fields.FloatField')()),
            ('tnr', self.gf('django.db.models.fields.FloatField')()),
            ('acc', self.gf('django.db.models.fields.FloatField')()),
            ('mcc', self.gf('django.db.models.fields.FloatField')()),
            ('tp', self.gf('django.db.models.fields.IntegerField')()),
            ('fp', self.gf('django.db.models.fields.IntegerField')()),
            ('tn', self.gf('django.db.models.fields.IntegerField')()),
            ('fn', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('corsair', ['PredictionStatistics'])


    def backwards(self, orm):
        
        # Deleting model 'TrainingSet'
        db.delete_table('corsair_trainingset')

        # Removing M2M table for field user_profiles on 'TrainingSet'
        db.delete_table('corsair_trainingset_user_profiles')

        # Removing M2M table for field ratings on 'TrainingSet'
        db.delete_table('corsair_trainingset_ratings')

        # Deleting model 'PredictionStatistics'
        db.delete_table('corsair_predictionstatistics')


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
        'corsair.predictionstatistics': {
            'Meta': {'object_name': 'PredictionStatistics'},
            'acc': ('django.db.models.fields.FloatField', [], {}),
            'classifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discrimination_bound': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'fn': ('django.db.models.fields.IntegerField', [], {}),
            'fp': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mcc': ('django.db.models.fields.FloatField', [], {}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'n_folds': ('django.db.models.fields.IntegerField', [], {}),
            'npv': ('django.db.models.fields.FloatField', [], {}),
            'ppv': ('django.db.models.fields.FloatField', [], {}),
            'raw_data': ('picklefield.fields.PickledObjectField', [], {}),
            'tn': ('django.db.models.fields.IntegerField', [], {}),
            'tnr': ('django.db.models.fields.FloatField', [], {}),
            'tp': ('django.db.models.fields.IntegerField', [], {}),
            'tpr': ('django.db.models.fields.FloatField', [], {}),
            'training_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['corsair.TrainingSet']"})
        },
        'corsair.trainingset': {
            'Meta': {'object_name': 'TrainingSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['twitterauth.Rating']", 'null': 'True', 'blank': 'True'}),
            'user_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['twitterauth.UserProfile']", 'symmetrical': 'False'})
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
            'content_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_hyperlink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashtags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['status.Hashtag']", 'null': 'True', 'blank': 'True'}),
            'hyperlinks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['status.Hyperlink']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'in_reply_to_status': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'status_replies'", 'null': 'True', 'to': "orm['status.Status']"}),
            'in_reply_to_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_replies'", 'null': 'True', 'to': "orm['twitterauth.UserProfile']"}),
            'punctuation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterauth.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'twitterauth.rating': {
            'Meta': {'ordering': "['-rated_time']", 'object_name': 'Rating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rated_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['status.Status']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterauth.UserProfile']"})
        },
        'twitterauth.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'active_classifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'classifier_version': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['status.Status']", 'symmetrical': 'False', 'through': "orm['twitterauth.Rating']", 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'training_statuses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['status.Status']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['corsair']
