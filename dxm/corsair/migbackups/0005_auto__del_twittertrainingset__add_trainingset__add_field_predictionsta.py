# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TwitterTrainingSet'
        db.delete_table('corsair_twittertrainingset')

        # Removing M2M table for field ratings on 'TwitterTrainingSet'
        db.delete_table('corsair_twittertrainingset_ratings')

        # Removing M2M table for field users on 'TwitterTrainingSet'
        db.delete_table('corsair_twittertrainingset_users')

        # Adding model 'TrainingSet'
        db.create_table('corsair_trainingset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('corsair', ['TrainingSet'])

        # Adding M2M table for field users on 'TrainingSet'
        db.create_table('corsair_trainingset_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trainingset', models.ForeignKey(orm['corsair.trainingset'], null=False)),
            ('twitteruserprofile', models.ForeignKey(orm['twitter.twitteruserprofile'], null=False))
        ))
        db.create_unique('corsair_trainingset_users', ['trainingset_id', 'twitteruserprofile_id'])

        # Adding M2M table for field ratings on 'TrainingSet'
        db.create_table('corsair_trainingset_ratings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trainingset', models.ForeignKey(orm['corsair.trainingset'], null=False)),
            ('rating', models.ForeignKey(orm['twitter.rating'], null=False))
        ))
        db.create_unique('corsair_trainingset_ratings', ['trainingset_id', 'rating_id'])

        # Adding field 'PredictionStatistics.training_set'
        db.add_column('corsair_predictionstatistics', 'training_set', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['corsair.TrainingSet']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'TwitterTrainingSet'
        db.create_table('corsair_twittertrainingset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
        ))
        db.send_create_signal('corsair', ['TwitterTrainingSet'])

        # Adding M2M table for field ratings on 'TwitterTrainingSet'
        db.create_table('corsair_twittertrainingset_ratings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('twittertrainingset', models.ForeignKey(orm['corsair.twittertrainingset'], null=False)),
            ('rating', models.ForeignKey(orm['twitter.rating'], null=False))
        ))
        db.create_unique('corsair_twittertrainingset_ratings', ['twittertrainingset_id', 'rating_id'])

        # Adding M2M table for field users on 'TwitterTrainingSet'
        db.create_table('corsair_twittertrainingset_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('twittertrainingset', models.ForeignKey(orm['corsair.twittertrainingset'], null=False)),
            ('twitteruserprofile', models.ForeignKey(orm['twitter.twitteruserprofile'], null=False))
        ))
        db.create_unique('corsair_twittertrainingset_users', ['twittertrainingset_id', 'twitteruserprofile_id'])

        # Deleting model 'TrainingSet'
        db.delete_table('corsair_trainingset')

        # Removing M2M table for field users on 'TrainingSet'
        db.delete_table('corsair_trainingset_users')

        # Removing M2M table for field ratings on 'TrainingSet'
        db.delete_table('corsair_trainingset_ratings')

        # Deleting field 'PredictionStatistics.training_set'
        db.delete_column('corsair_predictionstatistics', 'training_set_id')


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
            'Meta': {'ordering': "['-created']", 'object_name': 'PredictionStatistics'},
            'acc': ('django.db.models.fields.FloatField', [], {}),
            'auc': ('django.db.models.fields.FloatField', [], {}),
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
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['twitter.Rating']", 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['twitter.TwitterUserProfile']", 'symmetrical': 'False'})
        },
        'profile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
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

    complete_apps = ['corsair']
