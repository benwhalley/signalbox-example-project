# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionAsset'
        db.create_table('ask_questionasset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ask.Question'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('asset', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ask', ['QuestionAsset'])


        # Changing field 'Instrument.name'
        db.alter_column('ask_instrument', 'name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=255))

    def backwards(self, orm):
        # Deleting model 'QuestionAsset'
        db.delete_table('ask_questionasset')


        # Changing field 'Instrument.name'
        db.alter_column('ask_instrument', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, null=True))

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
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
        'ask.questionasset': {
            'Meta': {'object_name': 'QuestionAsset'},
            'asset': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ask.Question']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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