from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from challenge.models import Challenge

urlpatterns = patterns('',
    (r'^$',
     ListView.as_view(
         queryset = Challenge.objects.order_by('-create_date')[:25],
            context_object_name='top25_challenge_list',
            template_name='challenge/index.html')),
    (r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Challenge,
            template_name='challenge/detail.html')),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Challenge,
            template_name='challenge/solution.html'),
        name='challenge_results'),
    (r'^(?P<challenge_id>\d+)/submit/$', 'challenge.views.submit'),
    (r'^tags/$', 'challenge.views.tags'),
    (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$','challenge.views.with_tag')
)
