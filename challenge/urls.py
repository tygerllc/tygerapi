from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from challenge.models import Challenge
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    (r'^$',
     login_required(ListView.as_view(
         queryset = Challenge.objects.order_by('-create_date')[:25],
         context_object_name='top25_challenge_list',
         template_name='challenge/templates/challenge_list.html'))),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Challenge,
            template_name='challenge/templates/challenge_solutions_list.html'),
            name='challenge_results'),
    (r'^(?P<challenge_id>\d+)/submit/$',
        'challenge.views.submit'),
    (r'^tags/$',
        'challenge.views.tags'),
    (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$',
        'challenge.views.with_tag'),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/$',
        login_required(DetailView.as_view(
            model=Challenge,
            template_name='challenge/templates/challenge_detail.html')))
)
