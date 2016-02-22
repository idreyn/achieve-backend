# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table('quiz_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='MC', max_length=2)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('choices', self.gf('django.db.models.fields.TextField')()),
            ('correct', self.gf('django.db.models.fields.TextField')()),
            ('incorrect_explanation', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('quiz', ['Question'])

        # Adding model 'Quiz'
        db.create_table('quiz_quiz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('quiz', ['Quiz'])

        # Adding M2M table for field questions on 'Quiz'
        m2m_table_name = db.shorten_name('quiz_quiz_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quiz', models.ForeignKey(orm['quiz.quiz'], null=False)),
            ('question', models.ForeignKey(orm['quiz.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['quiz_id', 'question_id'])

        # Adding model 'QuizKey'
        db.create_table('quiz_quizkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
            ('achiever', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Achiever'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('quiz', ['QuizKey'])

        # Adding model 'Response'
        db.create_table('quiz_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Question'])),
            ('response', self.gf('django.db.models.fields.TextField')()),
            ('is_correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('quiz', ['Response'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table('quiz_question')

        # Deleting model 'Quiz'
        db.delete_table('quiz_quiz')

        # Removing M2M table for field questions on 'Quiz'
        db.delete_table(db.shorten_name('quiz_quiz_questions'))

        # Deleting model 'QuizKey'
        db.delete_table('quiz_quizkey')

        # Deleting model 'Response'
        db.delete_table('quiz_response')


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'choices': ('django.db.models.fields.TextField', [], {}),
            'correct': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incorrect_explanation': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'MC'", 'max_length': '2'})
        },
        'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['quiz.Question']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
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