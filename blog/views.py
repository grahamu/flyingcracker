from django.http import HttpResponse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

def upload_file(request):
    if request.is_ajax():
        if 'file' in request.FILES:
            file = request.FILES['file']
            # Other data on the request.FILES dictionary:
            filesize = len(file['content'])
            filetype = file['content-type']
            filename = file['filename']

            filepath ='%s/%s' % (settings.STATIC_ROOT, filename)
            fd = open(filepath, 'wb')
            fd.write(file['content'])
            fd.close()
            fileurl = '%s%s' % (settings.STATIC_URL, filename)
            result = {"status": "UPLOADED", "image_url": fileurl}
        else:
            result = {"status": "upload failed"}

        json = simplejson.dumps(result, cls=DjangoJSONEncoder)
        return HttpResponse(json, mimetype='text/html')  # try mimetype='application/javascript'
    else:
        return HttpResponse('sorry')
