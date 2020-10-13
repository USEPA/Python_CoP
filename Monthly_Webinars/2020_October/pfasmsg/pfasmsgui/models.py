"""
models.py - Demo model for Django demo

Terry N. Brown Brown.TerryN@epa.gov Fri 09/04/2020 
"""
from django.db import models

# Create your models here.

PRIORITIES = (
    (0, 'High'),
    (1, 'Medium'),
    (2, 'Low'),
)
PRIORITY = {v: k for k, v in PRIORITIES}


class PFASMsgRecord(models.Model):

    # IP number from which message was received
    ip = models.CharField(max_length=40)  # covers IP6
    # time at which message was received
    timestamp = models.DateTimeField()
    # the message text
    message = models.CharField(max_length=140)
    # message priority
    priority = models.IntegerField(
        choices=PRIORITIES, default=PRIORITY['Medium']
    )

    def __str__(self):
        """Provides meaningful representation in admin. panel instead of
        <PFASMsgRecord: 3>
        """
        return f"{self.message}"
