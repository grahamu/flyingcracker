
from south.db import db
from django.db import models
from fantasy.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Result.entered_by'
        db.add_column('fantasy_result', 'entered_by', orm['fantasy.result:entered_by'])



    def backwards(self, orm):

        # Deleting field 'Result.entered_by'
        db.delete_column('fantasy_result', 'entered_by_id')



    models = {
        'serviceclient.serviceclient': {
            'date_joined': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2009, 7, 6)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'db_index': 'True'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 7, 6, 10, 56, 25, 919000)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 7, 6, 10, 56, 25, 919000)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'scoresys.scoringsystem': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'num_places': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'serviceclient.serviceclientuserprofile': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClient']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        },
        'fantasy.result': {
            'Meta': {'unique_together': "(('competitor', 'event', 'result'),)"},
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Competitor']"}),
            'entered_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClientUserProfile']", 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fantasy.series': {
            'competitor_label': ('django.db.models.fields.CharField', [], {'default': "'Driver'", 'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'event_label': ('django.db.models.fields.CharField', [], {'default': "'Race'", 'max_length': '50'}),
            'guess_once_per_series': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'guesses': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['fantasy.Guess']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_only': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'num_guesses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'only_members_can_view': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClientUserProfile']"}),
            'scoring_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scoresys.ScoringSystem']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'users_enter_competitors': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'fantasy.competitor': {
            'Meta': {'unique_together': "(('name', 'series'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Series']"})
        },
        'fantasy.event': {
            'Meta': {'unique_together': "(('name', 'series'),)"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'guess_deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'guesses': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['fantasy.Guess']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'result_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Series']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'fantasy.guess': {
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Competitor']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClientUserProfile']"})
        }
    }

    complete_apps = ['fantasy']
