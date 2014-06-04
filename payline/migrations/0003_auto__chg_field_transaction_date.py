# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Transaction.date'
        db.alter_column(u'payline_transaction', 'date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Transaction.date'
        db.alter_column(u'payline_transaction', 'date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 4, 0, 0)))

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
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'order_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'8894e52a-4f87-439f-8e18-a384b53481b4'", 'unique': 'True', 'max_length': '36'}),
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
            'wallet_id': ('django.db.models.fields.CharField', [], {'default': "'15512853-5495-4750-9ef5-30b777b01a42'", 'unique': 'True', 'max_length': '36', 'db_index': 'True'})
        }
    }

    complete_apps = ['payline']