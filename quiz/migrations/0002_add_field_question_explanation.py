# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.explanation'
        db.add_column('quiz_question', 'explanation',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.explanation'
        db.delete_column('quiz_question', 'explanation')


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'choices': ('django.db.models.fields.TextField', [], {}),
            'correct': ('django.db.models.fields.TextField', [], {}),
            'explanation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'MC'", 'max_length': '2'})
        },
        'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['quiz.Question']", 'symmetrical': 'False'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'quiz.quizkey': {
            'Meta': {'object_name': 'QuizKey'},
            'achiever': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roster.Achiever']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Quiz']"})
        },
        'quiz.response': {
            'Meta': {'object_name': 'Response'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Question']"}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Quiz']"}),
            'response': ('django.db.models.fields.TextField', [], {})
        },
        'roster.achiever': {
            'Meta': {'object_name': 'Achiever'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['quiz']