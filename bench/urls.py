from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from bench.models import Bench, CodingRegion
from bench.views import BenchListView, BenchDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    (r'^$',
        login_required(BenchListView.as_view())),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/$',
        login_required(BenchDetailView.as_view()))
    )
