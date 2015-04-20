
from south.db import db
from django.db import models
from fantasy.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Competitor'
        db.create_table('fantasy_competitor', (
            ('series', orm['fantasy.Competitor:series']),
            ('id', orm['fantasy.Competitor:id']),
            ('name', orm['fantasy.Competitor:name']),
        ))
        db.send_create_signal('fantasy', ['Competitor'])

        # Adding model 'Event'
        db.create_table('fantasy_event', (
            ('result_locked', orm['fantasy.Event:result_locked']),
            ('description', orm['fantasy.Event:description']),
            ('series', orm['fantasy.Event:series']),
            ('start_time', orm['fantasy.Event:start_time']),
            ('start_date', orm['fantasy.Event:start_date']),
            ('guess_deadline', orm['fantasy.Event:guess_deadline']),
            ('location', orm['fantasy.Event:location']),
            ('id', orm['fantasy.Event:id']),
            ('name', orm['fantasy.Event:name']),
        ))
        db.send_create_signal('fantasy', ['Event'])

        # Adding model 'Series'
        db.create_table('fantasy_series', (
            ('status', orm['fantasy.Series:status']),
            ('only_members_can_view', orm['fantasy.Series:only_members_can_view']),
            ('event_label', orm['fantasy.Series:event_label']),
            ('description', orm['fantasy.Series:description']),
            ('end_date', orm['fantasy.Series:end_date']),
            ('competitor_label', orm['fantasy.Series:competitor_label']),
            ('start_date', orm['fantasy.Series:start_date']),
            ('users_enter_competitors', orm['fantasy.Series:users_enter_competitors']),
            ('num_guesses', orm['fantasy.Series:num_guesses']),
            ('invite_only', orm['fantasy.Series:invite_only']),
            ('owner', orm['fantasy.Series:owner']),
            ('scoring_system', orm['fantasy.Series:scoring_system']),
            ('id', orm['fantasy.Series:id']),
            ('name', orm['fantasy.Series:name']),
        ))
        db.send_create_signal('fantasy', ['Series'])

        # Adding model 'Guess'
        db.create_table('fantasy_guess', (
            ('event', orm['fantasy.Guess:event']),
            ('competitor', orm['fantasy.Guess:competitor']),
            ('id', orm['fantasy.Guess:id']),
            ('user', orm['fantasy.Guess:user']),
        ))
        db.send_create_signal('fantasy', ['Guess'])

        # Adding model 'Result'
        db.create_table('fantasy_result', (
            ('place', orm['fantasy.Result:place']),
            ('competitor', orm['fantasy.Result:competitor']),
            ('id', orm['fantasy.Result:id']),
            ('event', orm['fantasy.Result:event']),
        ))
        db.send_create_signal('fantasy', ['Result'])

        # Creating unique_together for [name, series] on Competitor.
        db.create_unique('fantasy_competitor', ['name', 'series_id'])

        # Creating unique_together for [competitor, event] on Result.
        db.create_unique('fantasy_result', ['competitor_id', 'event_id'])

        # Creating unique_together for [name, series] on Event.
        db.create_unique('fantasy_event', ['name', 'series_id'])



    def backwards(self, orm):

        # Deleting model 'Competitor'
        db.delete_table('fantasy_competitor')

        # Deleting model 'Event'
        db.delete_table('fantasy_event')

        # Deleting model 'Series'
        db.delete_table('fantasy_series')

        # Deleting model 'Guess'
        db.delete_table('fantasy_guess')

        # Deleting model 'Result'
        db.delete_table('fantasy_result')

        # Deleting unique_together for [name, series] on Competitor.
        db.delete_unique('fantasy_competitor', ['name', 'series_id'])

        # Deleting unique_together for [competitor, event] on Result.
        db.delete_unique('fantasy_result', ['competitor_id', 'event_id'])

        # Deleting unique_together for [name, series] on Event.
        db.delete_unique('fantasy_event', ['name', 'series_id'])



    models = {
        'serviceclient.serviceclient': {
            'date_joined': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2009, 7, 1)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'db_index': 'True'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 7, 1, 14, 47, 44, 770000)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 7, 1, 14, 47, 44, 770000)'}),
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
        'serviceclient.usergroupuserprofile': {
            'date_added': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2009, 7, 1)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_group_profile_set'", 'to': "orm['serviceclient.UserGroup']"}),
            'user_perm': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_group_profile_set'", 'to': "orm['serviceclient.ServiceClientUserProfile']"})
        },
        'serviceclient.usergroup': {
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'service_client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClient']"})
        },
        'serviceclient.serviceclientuserprofile': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClient']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        },
        'fantasy.result': {
            'Meta': {'unique_together': "(('competitor', 'event'),)"},
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Competitor']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.PositiveIntegerField', [], {})
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
            'guess_deadline': ('django.db.models.fields.DateTimeField', [], {}),
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
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serviceclient.ServiceClientUserProfile']"})
        }
    }

    complete_apps = ['serviceclient', 'fantasy']
