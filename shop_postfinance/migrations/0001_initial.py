# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PostfinanceIPN'
        db.create_table('shop_postfinance_postfinanceipn', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orderID', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('PM', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ACCEPTANCE', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('STATUS', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('CARDNO', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('CN', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('TRXDATE', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('PAYID', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('NCERROR', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('BRAND', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('IPCTY', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('CCCTY', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ECI', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('CVCCheck', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('AAVCheck', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('VC', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('IP', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('SHASIGN', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('shop_postfinance', ['PostfinanceIPN'])


    def backwards(self, orm):
        
        # Deleting model 'PostfinanceIPN'
        db.delete_table('shop_postfinance_postfinanceipn')


    models = {
        'shop_postfinance.postfinanceipn': {
            'AAVCheck': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ACCEPTANCE': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'BRAND': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CARDNO': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CCCTY': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CN': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CVCCheck': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ECI': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'IP': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'IPCTY': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'PostfinanceIPN'},
            'NCERROR': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'PAYID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'PM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SHASIGN': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'STATUS': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'TRXDATE': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VC': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orderID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shop_postfinance']
