from celery.task import PeriodicTask
from celery.schedules import crontab

from .models import FileUploadMessage, WebhookLog


class ProcessFileUploadMessages(PeriodicTask):
    run_every = crontab(minute=0, hour='*/3')  # this will run once every 3 hours
    def run(self, **kwargs):
        unprocessed_trans = self.get_transactions_to_process()

        for transaction in unprocessed_transactions:
            try:

                self.process_trans(transaction)
                transaction.status = WebhookLog.PROCESSED
                transaction.save()

            except Exception:
                transaction.status = WebhookLog.ERROR
                transaction.save()

    def get_transactions_to_process(self):
        return WebhookLog.objects.filter(
            event_name__in=self.event_names,
            status=WebhookLog.UNPROCESSED
        )

    def process_trans(self, transaction):
        transaction_body = json.loads(transaction.body)
        if transaction_body['is_image']:
            uploadMessageObject = ImageUploadMessage.objects.create(
                    webhook_transaction = transaction,                 
                    uuid = transaction_body['uuid'],
                    is_image = transaction_body['is_image'],
                    filename = transaction_body['filename'],
                    is_stored = transaction_body['is_stored'],
                    done = transaction_body['done'],
                    file_id = transaction_body['file_id'],
                    original_filename = transaction_body['original_filename'],
                    image_info = transaction_body['image_info'],
                    is_ready = transaction_body['is_ready'],
                    total = transaction_body['total'],
                    mime_type = transaction_body['mime_type'],
                    size = transaction_body['size'],
                    file = transaction_body['file'],
                    orientation = transaction_body['orientation'],
                    imgformat =  transaction_body['imgformat'],
                    height = transaction_body['height'],
                    width = transaction_body['width'],
                    geo_location =  transaction_body['geo_location'],
                    datetime_original = transaction_body['datetime_original'],
                    dpi = transaction_body['dpi']
                                                                    )
        else:
            uploadMessageObject = FileUploadMessage.objects.create(
                    webhook_transaction = transaction,                 
                    uuid = transaction_body['uuid'],
                    is_image = transaction_body['is_image'],
                    filename = transaction_body['filename'],
                    is_stored = transaction_body['is_stored'],
                    done = transaction_body['done'],
                    file_id = transaction_body['file_id'],
                    original_filename = transaction_body['original_filename'],
                    image_info = transaction_body['image_info'],
                    is_ready = transaction_body['is_ready'],
                    total = transaction_body['total'],
                    mime_type = transaction_body['mime_type'],
                    size = transaction_body['size'],
                    file = transaction_body['file']
                                                                   )
        
        return uploadMessageObject
