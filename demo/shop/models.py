from django.db import models
from uuid import uuid4


def get_uuid():
    return str(uuid4())


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=36, default=get_uuid)
    amount = models.DecimalField(max_digits=12, decimal_places=6)

    def __unicode__(self):
        return self.identifier
