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

    def __unicode__(self):
        return u'{0}'.format(self.date_event_generated)

class FileUploadMessage(models.Model):

    webhook_transaction = models.OneToOneField(WebhookLog)
    date_processed = models.DateTimeField(default=timezone.now)
    uuid = models.CharField(max_length=255)
    is_image = models.CharField(max_length=250)
    filename = models.CharField(max_length=250)
    is_stored = models.CharField(max_length=250)
    done = models.CharField(max_length=250)
    file_id = models.CharField(max_length=250)
    original_filename = models.CharField(max_length=250)
    image_info = models.CharField(max_length=255)
    is_ready = models.TextField()
    total = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    size = models.FloatField(max_length=255)
    file = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{}'.format(self.uuid)

class ImageUploadMessage(FileUploadMessage):

       orientation = models.CharField(max_length=255)
       imgformat =  models.CharField(max_length=255)
       height = models.FloatField(max_length=255)
       width = models.FloatField(max_length=255)
       geo_location =  models.CharField(max_length=255)
       datetime_original = models.DateTimeField(),
       dpi = models.FloatField(max_length=255)

            


class Photo(models.Model):

    title = models.CharField(max_length=255)
    photo = ImageField()





