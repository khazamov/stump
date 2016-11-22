from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
import json
import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pyuploadcare.api_resources import File
import pdb
from .models import WebhookLog


def copy_to_azure(file_uuid):
  try: 
    CDN_BASE="https://ucarecdn.com/"
    file_url = CDN_BASE + file_uuid + '/'
    block_blob_service = BlockBlobService(account_name='uploadcaretest', 
    account_key='SGpgQ8GVi6NETpZSFAkqtWacLUim5Fdsw7z2cu8Kk6Esm4cwAJwvy705tNohArQPjbVkW6wXwzXekW5U22fzWg==')
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
    print("Copying to S3 file uuid" + file_uuid)
    file = File(file_uuid);
    file.copy(None, 'bucner123', 'true');
  except Exception, e:
         print (e.message);
  else:
        pass
  finally:
        pass


@csrf_exempt
@require_POST
def webhook(request):
  try:
 
    jsondata = request.body
    data = json.loads(jsondata)
    meta = copy.copy(request.META)
    for k, v in meta.items():
        if not isinstance(v, basestring):
            del meta[k]
    #pdb.set_trace()
    WebhookLog.objects.create(
    date_generated=timezone.now(),
        body=jsondata,
        request_meta=json.dumps(meta),
        is_image = data['data']['is_image']
    )
    
    #copy_to_s3(data['data']['uuid'])

    return HttpResponse(status=200)
       
  except Exception, e:
         print (e.message);
  else:
        pass
  finally:
        pass



    
