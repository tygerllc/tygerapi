# This also imports the include function
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^challenge/', include('challenge.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^bench/', include('bench.urls')),
    (r'^tutorial/', redirect_to, {'url': '/challenge/tag/tutorial/'}),
    (r'^logout/', 'challenge.views.logout_view'),
    (r'^login/', 'challenge.views.login_view'),
    url(r'^admin/', include(admin.site.urls)),
)