from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^challenge/', include('challenge.urls')),
	(r'^admin/', include(admin.site.urls)),
)

