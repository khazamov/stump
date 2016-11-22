from __future__ import unicode_literals
from django.db import models
from pyuploadcare.dj.models import ImageField
from django.db import models
from django.utils import timezone
from django_hstore import hstore


class WebhookLog(models.Model):
    UNPROCESSED = 1
    PROCESSED = 2
    ERROR = 3

    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    date_generated = models.DateTimeField()
    date_received = models.DateTimeField(default=timezone.now)
    body = models.CharField(max_length=4096, default='')
    request_meta = models.CharField(max_length=4096, default='')
    status = models.CharField(max_length=250, choices=STATUSES, default=UNPROCESSED)
    is_image = models.BooleanField(default=False)
    objects = hstore.HStoreManager()

    # def __unicode__(self):
    #     return u'{0}'.format(self.date_event_generated)
class UploadMessage(models.Model):

    webhook_transaction = models.OneToOneField(WebhookLog)
    date_processed = models.DateTimeField(default=timezone.now)
    uuid = models.CharField(max_length=255)
    filename = models.CharField(max_length=250)
    is_stored = models.BooleanField()
    done = models.BigIntegerField()
    file_id = models.CharField(max_length=250)
    original_filename = models.CharField(max_length=255)
    is_ready = models.BooleanField()
    total = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    size = models.BigIntegerField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{}'.format(self.uuid)

class FileUploadMessage(UploadMessage):
    pass

class ImageUploadMessage(UploadMessage):
    orientation = models.CharField(max_length=255,null = True, default = None)
    imgformat =  models.CharField(max_length=255,null = True, default = None)
    height = models.IntegerField()
    width = models.IntegerField()
    geo_location =  models.CharField(max_length=255, null = True, default = None)
    datetime_original = models.DateTimeField(null = True, default = None)
    dpi = models.IntegerField(null = True, default = None)