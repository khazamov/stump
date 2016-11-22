
from celery.task import PeriodicTask
from celery.schedules import crontab
from azure.storage.blob import BlockBlobService
from stump.celery_app import app
from .models import FileUploadMessage,ImageUploadMessage, WebhookLog
import wget
from celery.utils.log import get_task_logger
from pyuploadcare.api_resources import File
import json
logger = get_task_logger(__name__)

#todo - copy from url, error handling
def copy_to_azure(file_uuid):
  try: 
    CDN_BASE="https://ucarecdn.com/"
    file_url = CDN_BASE + file_uuid + '/'
    block_blob_service = BlockBlobService(account_name='uploadcaretest',
                                          #take out account key to filesystem or database
    account_key='')
    block_blob_service.create_container('image_container')
    block_blob_service.set_container_acl('image_container', public_access=PublicAccess.Container)
    filename = wget.download(file_url)
    block_blob_service.create_blob_from_path('image_container',   uuid,   'filename', content_settings=ContentSettings(content_type='image/png'))
  except Exception, e:
         print (e.message);
  else:
        pass
  finally:
        pass

  
def copy_to_s3(file_uuid):
  try:
    # do additional processing,i.e add certain effects
    print("Copying to S3 file uuid " + file_uuid)
    logger.info("In the process of copying fileUUID "+str(file_uuid))
    file = File(file_uuid)
    response = file.copy(None, 'bucner123', 'true')
  except Exception, e:
         logger.info("An error while copying file to s3 storage: " +str(e))
  else:
        pass
  finally:
        pass




@app.task(name='stamper.tasks.ProcessFileUploadMessages')
class ProcessFileUploadMessages(PeriodicTask):
    run_every = crontab(minute='*', hour='*',day_of_week="*")  #  every minute
    def run(self, **kwargs):
        unprocessed_transactions = self.get_transactions_to_process()
        for transaction in unprocessed_transactions:
            try:
                uploadMessageObject = self.process_trans(transaction)
                transaction.status = WebhookLog.PROCESSED
                transaction.save()

            except Exception, e:
                logger.error("Error while processing transaction: " + str(e))
                transaction.status = WebhookLog.ERROR
                transaction.save()


    def get_transactions_to_process(self):
        logger.info("getting transactions to process")
        return WebhookLog.objects.filter(
            status=WebhookLog.UNPROCESSED
        )

    def process_trans(self, transaction):
        try:
            logger.info("actually processing a transaction.body ")
            transaction_hook_body = json.loads(transaction.body)
            transaction_body = transaction_hook_body['data']
            logger.info("preparing to copy file uuid: " + str(transaction_body['uuid']))
            copy_to_s3(transaction_body['uuid'])
            #copy_to_azure(transaction_body['uuid'])
            if transaction_body['is_image']:
                uploadMessageObject = ImageUploadMessage.objects.create(
                        webhook_transaction = transaction,
                        uuid = transaction_body['uuid'],
                        filename = transaction_body['filename'],
                        is_stored = transaction_body['is_stored'],
                        done = transaction_body['done'],
                        file_id = transaction_body['file_id'],
                        original_filename = transaction_body['original_filename'],
                        is_ready = transaction_body['is_ready'],
                        total = transaction_body['total'],
                        mime_type = transaction_body['mime_type'],
                        size = transaction_body['size'],
                        orientation = transaction_body['image_info']['orientation'],
                        imgformat =  transaction_body['image_info']['format'],
                        height = transaction_body['image_info']['height'],
                        width = transaction_body['image_info']['width'],
                        geo_location =  transaction_body['image_info']['geo_location'],
                        datetime_original = transaction_body['image_info']['datetime_original'],
                        dpi = transaction_body['image_info']['dpi']
                                                                        )
            else:
                uploadMessageObject = FileUploadMessage.objects.create(
                        webhook_transaction = transaction,
                        uuid = transaction_body['uuid'],
                        filename = transaction_body['filename'],
                        is_stored = transaction_body['is_stored'],
                        done = transaction_body['done'],
                        file_id = transaction_body['file_id'],
                        original_filename = transaction_body['original_filename'],
                        is_ready = transaction_body['is_ready'],
                        total = transaction_body['total'],
                        mime_type = transaction_body['mime_type'],
                        size = transaction_body['size']
               )
            uploadMessageObject.save()
            return uploadMessageObject
        except Exception, e:
            logger.error("Error while saving transaction "+  str(e))
        finally:
            logger.info("Just saved uploadMessageObject ")

