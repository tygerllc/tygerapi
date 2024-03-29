from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from challenge.models import Challenge
from challenge.views import ChallengeListViewRecent, ChallengeListViewBounty, ChallengeListViewVotes, ChallengeListViewOldestUnsolved, ChallengeListViewLibrary
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    (r'^$|^popular/?$',
     login_required(ChallengeListViewVotes.as_view())),
    (r'^top-bounty/?$',
     login_required(ChallengeListViewBounty.as_view())),
    (r'^recent/?$',
     login_required(ChallengeListViewRecent.as_view())),
    (r'^oldest-unsolved/?$',
     login_required(ChallengeListViewOldestUnsolved.as_view())),
    (r'^library/?$',
     login_required(ChallengeListViewLibrary.as_view())),
    (r'^tags/$',
        'challenge.views.tags'),
    (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$',
        'challenge.views.with_tag', {"sortOrder" : "most-recent"}),
    (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/(?P<sortOrder>[-_A-Za-z0-9]+)/$',
        'challenge.views.with_tag'),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/hints$',
        login_required(DetailView.as_view(
            model=Challenge,
            template_name='challenge_hints.html'))),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/talk$',
        login_required(DetailView.as_view(
            model=Challenge,
            template_name='challenge_discussion.html'))),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/solved$',
        login_required(DetailView.as_view(
            model=Challenge,
            template_name='challenge_solved.html'))),
    (r'^(?P<slug>[-_A-Za-z0-9]+)/$',
            login_required(DetailView.as_view(
                model=Challenge,
                template_name='challenge_detail.html')))

)
