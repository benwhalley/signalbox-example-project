# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table('ask_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('variable_name', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=32)),
            ('variable_label', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('choiceset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.ChoiceSet'], null=True, blank=True)),
            ('scoresheet', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='scoresheettoshow', null=True, to=orm['signalbox.ScoreSheet'])),
            ('help_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('always_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('audio', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('q_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('widget_kwargs', self.gf('jsonfield.fields.JSONField')(blank=True)),
            ('field_kwargs', self.gf('jsonfield.fields.JSONField')(blank=True)),
        ))
        db.send_create_signal('ask', ['Question'])

        # Adding model 'Choice'
        db.create_table('ask_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choiceset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.ChoiceSet'], null=True, blank=True)),
            ('is_default_value', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ask', ['Choice'])

        # Adding unique constraint on 'Choice', fields ['choiceset', 'score']
        db.create_unique('ask_choice', ['choiceset_id', 'score'])

        # Adding model 'ChoiceSet'
        db.create_table('ask_choiceset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('prompt_wording', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('ask', ['ChoiceSet'])

        # Adding model 'QuestionInAskPage'
        db.create_table('ask_questioninaskpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Question'])),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.AskPage'])),
            ('allow_not_applicable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('showif', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.ShowIf'], null=True, blank=True)),
        ))
        db.send_create_signal('ask', ['QuestionInAskPage'])

        # Adding model 'QuestionInInstrument'
        db.create_table('ask_questionininstrument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Question'])),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Instrument'])),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('showif', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.ShowIf'], null=True, blank=True)),
        ))
        db.send_create_signal('ask', ['QuestionInInstrument'])

        # Adding model 'ShowIf'
        db.create_table('ask_showif', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('previous_question', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='previous_question', null=True, to=orm['ask.Question'])),
            ('summary_score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signalbox.ScoreSheet'], null=True, blank=True)),
            ('values', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('less_than', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('more_than', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('ask', ['ShowIf'])

        # Adding model 'StataSyntax'
        db.create_table('ask_statasyntax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Instrument'])),
            ('stata_syntax', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ask', ['StataSyntax'])

        # Adding model 'Instrument'
        db.create_table('ask_instrument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True)),
            ('citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('usage_information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('ask', ['Instrument'])

        # Adding unique constraint on 'Instrument', fields ['name']
        db.create_unique('ask_instrument', ['name'])

        # Adding model 'InstrumentInAskPage'
        db.create_table('ask_instrumentinaskpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Instrument'])),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('variable_prefix', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.AskPage'])),
            ('showif', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.ShowIf'], null=True, blank=True)),
            ('allow_not_applicable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('require_all', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ask', ['InstrumentInAskPage'])

        # Adding model 'AskPage'
        db.create_table('ask_askpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Asker'])),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('ask', ['AskPage'])

        # Adding unique constraint on 'AskPage', fields ['internal_name', 'asker']
        db.create_unique('ask_askpage', ['internal_name', 'asker_id'])

        # Adding model 'Asker'
        db.create_table('ask_asker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('page_title', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('show_progress', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hide_menu', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ask', ['Asker'])


    def backwards(self, orm):
        # Removing unique constraint on 'AskPage', fields ['internal_name', 'asker']
        db.delete_unique('ask_askpage', ['internal_name', 'asker_id'])

        # Removing unique constraint on 'Instrument', fields ['name']
        db.delete_unique('ask_instrument', ['name'])

        # Removing unique constraint on 'Choice', fields ['choiceset', 'score']
        db.delete_unique('ask_choice', ['choiceset_id', 'score'])

        # Deleting model 'Question'
        db.delete_table('ask_question')

        # Deleting model 'Choice'
        db.delete_table('ask_choice')

        # Deleting model 'ChoiceSet'
        db.delete_table('ask_choiceset')

        # Deleting model 'QuestionInAskPage'
        db.delete_table('ask_questioninaskpage')

        # Deleting model 'QuestionInInstrument'
        db.delete_table('ask_questionininstrument')

        # Deleting model 'ShowIf'
        db.delete_table('ask_showif')

        # Deleting model 'StataSyntax'
        db.delete_table('ask_statasyntax')

        # Deleting model 'Instrument'
        db.delete_table('ask_instrument')

        # Deleting model 'InstrumentInAskPage'
        db.delete_table('ask_instrumentinaskpage')

        # Deleting model 'AskPage'
        db.delete_table('ask_askpage')

        # Deleting model 'Asker'
        db.delete_table('ask_asker')


    models = {
        'ask.asker': {
            'Meta': {'object_name': 'Asker'},
            'hide_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'show_progress': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'ask.askpage': {
            'Meta': {'ordering': "['order']", 'unique_together': "(['internal_name', 'asker'],)", 'object_name': 'AskPage'},
            'asker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Asker']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instruments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ask.Instrument']", 'through': "orm['ask.InstrumentInAskPage']", 'symmetrical': 'False'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ask.Question']", 'through': "orm['ask.QuestionInAskPage']", 'symmetrical': 'False'})
        },
        'ask.choice': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('choiceset', 'score'),)", 'object_name': 'Choice'},
            'choiceset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.ChoiceSet']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default_value': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        },
        'ask.choiceset': {
            'Meta': {'ordering': "['name']", 'object_name': 'ChoiceSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'prompt_wording': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'ask.instrument': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['name'],)", 'object_name': 'Instrument'},
            'citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ask.Question']", 'through': "orm['ask.QuestionInInstrument']", 'symmetrical': 'False'}),
            'usage_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'ask.instrumentinaskpage': {
            'Meta': {'ordering': "['instrument__name']", 'object_name': 'InstrumentInAskPage'},
            'allow_not_applicable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Instrument']"}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.AskPage']"}),
            'require_all': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'showif': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.ShowIf']", 'null': 'True', 'blank': 'True'}),
            'variable_prefix': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        'ask.question': {
            'Meta': {'ordering': "['variable_name']", 'object_name': 'Question'},
            'always_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'choiceset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.ChoiceSet']", 'null': 'True', 'blank': 'True'}),
            'field_kwargs': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'q_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'scoresheet': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scoresheettoshow'", 'null': 'True', 'to': "orm['signalbox.ScoreSheet']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'variable_label': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'variable_name': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '32'}),
            'widget_kwargs': ('jsonfield.fields.JSONField', [], {'blank': 'True'})
        },
        'ask.questioninaskpage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'QuestionInAskPage'},
            'allow_not_applicable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.AskPage']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Question']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'showif': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.ShowIf']", 'null': 'True', 'blank': 'True'})
        },
        'ask.questionininstrument': {
            'Meta': {'ordering': "('order',)", 'object_name': 'QuestionInInstrument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Instrument']"}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Question']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'showif': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.ShowIf']", 'null': 'True', 'blank': 'True'})
        },
        'ask.showif': {
            'Meta': {'object_name': 'ShowIf'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'less_than': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'more_than': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'previous_question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous_question'", 'null': 'True', 'to': "orm['ask.Question']"}),
            'summary_score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signalbox.ScoreSheet']", 'null': 'True', 'blank': 'True'}),
            'values': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'ask.statasyntax': {
            'Meta': {'object_name': 'StataSyntax'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Instrument']"}),
            'stata_syntax': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'signalbox.scoresheet': {
            'Meta': {'object_name': 'ScoreSheet'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'variables': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'varsinscoresheet'", 'symmetrical': 'False', 'to': "orm['ask.Question']"})
        }
    }

    complete_apps = ['ask']