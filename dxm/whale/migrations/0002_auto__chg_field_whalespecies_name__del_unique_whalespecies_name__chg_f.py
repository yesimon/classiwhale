# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Whale', fields ['name']
        db.delete_unique('whale_whale', ['name'])

        # Removing unique constraint on 'WhaleSpecies', fields ['name']
        db.delete_unique('whale_whalespecies', ['name'])

        # Changing field 'WhaleSpecies.name'
        db.alter_column('whale_whalespecies', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Whale.name'
        db.alter_column('whale_whale', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))


    def backwards(self, orm):
        
        # Changing field 'WhaleSpecies.name'
        db.alter_column('whale_whalespecies', 'name', self.gf('django.db.models.fields.CharField')(default='Baby Whale', max_length=50, unique=True))

        # Adding unique constraint on 'WhaleSpecies', fields ['name']
        db.create_unique('whale_whalespecies', ['name'])

        # Changing field 'Whale.name'
        db.alter_column('whale_whale', 'name', self.gf('django.db.models.fields.CharField')(default='My Whale', max_length=50, unique=True))

        # Adding unique constraint on 'Whale', fields ['name']
        db.create_unique('whale_whale', ['name'])


    models = {
        'whale.whale': {
            'Meta': {'object_name': 'Whale'},
            'exp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'My Whale'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whale.WhaleSpecies']", 'null': 'True', 'blank': 'True'})
        },
        'whale.whalespecies': {
            'Meta': {'object_name': 'WhaleSpecies'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Baby Whale'", 'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['whale']
