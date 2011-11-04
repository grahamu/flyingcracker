
from south.db import db
from django.db import models
from scoresys.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'ResultPoints.rank'
        db.add_column('scoresys_resultpoints', 'rank', orm['scoresys.resultpoints:rank'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'ResultPoints.rank'
        db.delete_column('scoresys_resultpoints', 'rank')
        
    
    
    models = {
        'scoresys.resultpoints': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scoresys.ScoringSystem']"})
        },
        'scoresys.scoringsystem': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'num_places': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }
    
    complete_apps = ['scoresys']
