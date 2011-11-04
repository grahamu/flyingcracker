
from south.db import db
from django.db import models
from scoresys.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ResultPoints'
        db.create_table('scoresys_resultpoints', (
            ('system', orm['scoresys.ResultPoints:system']),
            ('points', orm['scoresys.ResultPoints:points']),
            ('id', orm['scoresys.ResultPoints:id']),
            ('result', orm['scoresys.ResultPoints:result']),
        ))
        db.send_create_signal('scoresys', ['ResultPoints'])
        
        # Adding model 'ScoringSystem'
        db.create_table('scoresys_scoringsystem', (
            ('description', orm['scoresys.ScoringSystem:description']),
            ('num_places', orm['scoresys.ScoringSystem:num_places']),
            ('id', orm['scoresys.ScoringSystem:id']),
            ('name', orm['scoresys.ScoringSystem:name']),
        ))
        db.send_create_signal('scoresys', ['ScoringSystem'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ResultPoints'
        db.delete_table('scoresys_resultpoints')
        
        # Deleting model 'ScoringSystem'
        db.delete_table('scoresys_scoringsystem')
        
    
    
    models = {
        'scoresys.resultpoints': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
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
