from django.conf.urls.defaults import *
from bench.views import BenchListView, BenchDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    (r'^$',
        login_required(BenchListView.as_view())),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/$',
        login_required(BenchDetailView.as_view()))
    )
