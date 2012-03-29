# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Whale'
        db.create_table('whale_whale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('exp', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whale.WhaleSpecies'], null=True, blank=True)),
        ))
        db.send_create_signal('whale', ['Whale'])

        # Adding model 'WhaleSpecies'
        db.create_table('whale_whalespecies', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('whale', ['WhaleSpecies'])


    def backwards(self, orm):
        
        # Deleting model 'Whale'
        db.delete_table('whale_whale')

        # Deleting model 'WhaleSpecies'
        db.delete_table('whale_whalespecies')


    models = {
        'whale.whale': {
            'Meta': {'object_name': 'Whale'},
            'exp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whale.WhaleSpecies']", 'null': 'True', 'blank': 'True'})
        },
        'whale.whalespecies': {
            'Meta': {'object_name': 'WhaleSpecies'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['whale']
