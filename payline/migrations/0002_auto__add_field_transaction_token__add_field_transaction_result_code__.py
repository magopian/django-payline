# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Transaction', fields ['transaction_id']
        db.delete_unique(u'payline_transaction', ['transaction_id'])

        # Adding field 'Transaction.token'
        db.add_column(u'payline_transaction', 'token',
                      self.gf('django.db.models.fields.CharField')(default='da90cc83-129c-4911-a9de-0543194422d0', unique=True, max_length=36),
                      keep_default=False)

        # Adding field 'Transaction.result_code'
        db.add_column(u'payline_transaction', 'result_code',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True),
                      keep_default=False)

        # Adding field 'Transaction.order_type'
        db.add_column(u'payline_transaction', 'order_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, on_delete=models.SET_NULL),
                      keep_default=False)

        # Adding field 'Transaction.order_id'
        db.add_column(u'payline_transaction', 'order_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding index on 'Transaction', fields ['transaction_id']
        db.create_index(u'payline_transaction', ['transaction_id'])

        # Deleting field 'Transaction.token'
        db.delete_column(u'payline_transaction', 'token')

        # Deleting field 'Transaction.result_code'
        db.delete_column(u'payline_transaction', 'result_code')

        # Deleting field 'Transaction.order_type'
        db.delete_column(u'payline_transaction', 'order_type_id')

        # Deleting field 'Transaction.order_id'
        db.delete_column(u'payline_transaction', 'order_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'payline.transaction': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'order_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'d55a9b8b-12e0-463f-b475-d98f518c430b'", 'unique': 'True', 'max_length': '36'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
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
            'wallet_id': ('django.db.models.fields.CharField', [], {'default': "'b8af543e-261e-4c04-a2ef-f53c0c27d56b'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'})
        }
    }

    complete_apps = ['payline']
