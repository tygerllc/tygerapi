# This also imports the include function
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^challenge/', include('challenge.urls')),
    (r'^profile/', include('profiles.urls')),
    (r'^tutorial/', redirect_to, {'url': '/challenge/tag/tutorial/'}),
    url(r'^admin/', include(admin.site.urls)),
)