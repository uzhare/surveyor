from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
import datetime
from json_field import JSONField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust



class Thing(models.Model):
    key = models.CharField(max_length=512)
    value = JSONField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(default=datetime.datetime.now)
    modified  = models.DateTimeField(auto_now=True)



    @classmethod
    def has_key(klass, key, object_id=None, content_object=None):
        qs = klass.objects.filter(key=key)

        if object_id:
            qs = qs.objects.filter(object_id=object_id)

        if content_object:
            qs = qs.objects.filter(object_id=object_id)

        return bool(qs.count())
    
    @classmethod
    def get(klass, *args, **kwargs):
        key = kwargs.get('key', None)
        object_id = kwargs.get('object_id', None)
        content_object = kwargs.get('content_object', None)

        if key:
            return klass.objects.get(key=key)
        elif object_id and content_object:
            return klass.objects.filter(object_id=object_id,
                                        content_object=content_object)
        elif object_id and not content_object:
            return klass.objects.filter(object_id=object_id)
        elif content_object and not object_id:
            return klass.objects.filter(content_object=content_object)
        else:
            raise klass.DoesNotExist('No objects exist for given argument combination %s' % kwargs )


    def remove_key(klass, *args, **kwargs):
        key = kwargs.get('key', None)
        object_id = kwargs.get('object_id', None)
        content_object = kwargs.get('content_object', None)

        if key:
            return klass.objects.filter(key=key).delete()
        elif object_id and content_object:
            return klass.objects.filter(object_id=object_id,
                                        content_object=content_object).delete()
        elif object_id and not content_object:
            return klass.objects.filter(object_id=object_id)
        elif content_object and not object_id:
            return klass.objects.filter(content_object=content_object).delete()
        else:
            raise klass.DoesNotExist('No objects exist for given argument combination %s' % kwargs )


def valid_mobile_number(value):
    if not value.isdigit():
        raise ValidationError(u'%s is not a valid mobile number' % value)
    if len(value) > 10:
        raise ValidationError(u'Mobile number must be exactly 10 digits long')


class Profile(User):
    mobile_no = models.CharField(max_length=10, unique=True, validators=[valid_mobile_number])
    imei = models.CharField(max_length=128, unique=True) 


class Survey(models.Model):
    photo_original = models.ImageField(upload_to='photos')
    photo_display = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(400)], image_field='photo_original',
            format='JPEG', options={'quality': 90})
    photo_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(90)], image_field='photo_original',
            format='JPEG', options={'quality': 90},)

    video = models.FileField(upload_to='videos')
    user = models.ForeignKey(User)

    created = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now=True)

    def thumbnail(self):
        return """<img border="0" alt="" src= "/static/media/%s" height="40" /> """ %(self.photo_original.name)

    thumbnail.allow_tags = True



