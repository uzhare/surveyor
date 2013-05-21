from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from settings import local
from django.contrib import admin
admin.autodiscover()
from things.views import api_v1

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'surveyor.views.home', name='home'),
    # url(r'^surveyor/', include('surveyor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^api/v1/$', 'things.views.api_v1', name='api_v1'),
    url(r'^admin/', include(admin.site.urls)),

)
urlpatterns += staticfiles_urlpatterns()
if local.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': local.MEDIA_ROOT,
        }),
   )
