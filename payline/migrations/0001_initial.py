# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wallet'
        db.create_table(u'payline_wallet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet_id', self.gf('django.db.models.fields.CharField')(default='8307369f-25e2-4389-9beb-c6f3eb57c2fb', unique=True, max_length=36, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('card_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('card_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('card_expiry', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'payline', ['Wallet'])

        # Adding model 'Transaction'
        db.create_table(u'payline_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payline.Wallet'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, db_index=True)),
        ))
        db.send_create_signal(u'payline', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Wallet'
        db.delete_table(u'payline_wallet')

        # Deleting model 'Transaction'
        db.delete_table(u'payline_transaction')


    models = {
        u'payline.transaction': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payline.Wallet']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'payline.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'card_expiry': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'wallet_id': ('django.db.models.fields.CharField', [], {'default': "'877728af-8b3b-40c0-885b-4089476d6f4c'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'})
        }
    }

    complete_apps = ['payline']