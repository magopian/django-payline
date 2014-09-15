from django.contrib import admin
from . import models
from payline.models import Transaction


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'amount', 'created_at')

admin.site.register(models.Order, OrderAdmin)
admin.site.register(Transaction)
