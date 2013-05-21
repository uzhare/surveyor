import os
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import anyjson
import bleach


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
# TODO: 
@csrf_exempt
def api_v1(request):
    response_data = {}
    if request.method == 'POST':
        imei = request.POST.get('api_key', None)
        imei = bleach.clean(imei)
        #TODO: if imei not present reponse to app
        try:
            user = Profile.objects.get(imei=imei)
        except Exception, e:
            response_data['not_registered'] = "You are not a registered user"
            return HttpResponse(anyjson.serialize(response_data), mimetype='application/json')
        survey = Survey(user=user)
        survey.save()

        for key, value in request.POST.items():
            if key.startswith('tkey_'):
                key =  bleach.clean(key)
                value =  bleach.clean(value)
                try:
                    t = Thing(key=str(key.lstrip('tkey_')),value= value, content_object=survey)
                    t.save() 
                except Exception, e:
                    print e
        survey.original_photo = handle_uploaded_media(request.FILES['photo'], survey, "photos")
        survey.save()
        survey.video = handle_uploaded_media(request.FILES['video'], survey, "videos")
        survey.save()
        response_data['success'] = True
    return HttpResponse(anyjson.serialize(response_data), mimetype='application/json')


def handle_uploaded_media(file, survey, type='photos'):
    name, ext = os.path.splitext(file.name)
    filename = 'survey_%d_%s%s%s' % (22, survey.id, 
                                    survey.created.strftime('%Y%m%d%H%M%S'),
                                   ext)
    fspath = os.path.join(settings.MEDIA_ROOT, type,  filename)
    with open(fspath, 'wb+') as dest:
        for chunks in file.chunks():
            dest.write(chunks)

    return os.path.join(type, filename)


