from django.db import models
from uuid import uuid4


def get_uuid():
    return str(uuid4())


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = (
        ('pending', "Pending"),
        ('accepted', "Accepted"),
        ('cancelled', "Cancelled"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=36, default=get_uuid)
    amount = models.DecimalField(max_digits=12, decimal_places=6)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=STATUS_PENDING)

    def __unicode__(self):
        return self.identifier

    def validate(self):
        self.status = self.STATUS_ACCEPTED
        self.save()

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.save()
