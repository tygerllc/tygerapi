# This also imports the include function
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^challenge/?', include('challenge.urls')),
    (r'^api/', include('api.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^bench/?', include('bench.urls')),
    (r'^tutorial/?', 'challenge.views.tutorial'),
    (r'^logout/', 'challenge.views.logout_view'),
    (r'^login/', 'challenge.views.login_view'),
    (r'^about/', 'challenge.views.about_view'),
    (r'^contact/', 'challenge.views.contact_view'),
    (r'^thanks/', 'challenge.views.thanks_view'),
#    (r'^blog/', redirect_to, {'url': 'http://www.google.com'}),
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )