from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from challenge.models import Challenge, Criteria
from django.core.urlresolvers import reverse
from tagging.models import Tag, TaggedItem
import models
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

#TODO change solution view to list all solutions
#TODO Add view that selects a solution by a specific user.

@login_required()
def submit(request, challenge_id):
    c = get_object_or_404(Challenge, pk=challenge_id)
    try:
        selected_criteria = c.criteria_set.get(pk=request.POST['criteria'])
    except (KeyError, Challenge.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('/challenge/challenge_detail.html', {
            'challenge': c,
            'error_message': "No challenge selected.",
        }, context_instance=RequestContext(request))
    else:
        selected_criteria.status = not selected_criteria.status
        selected_criteria.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('challenge_results', args=(c.id,)))

@login_required()
def tags(request):
        return render_to_response('challenge/templates/challenges_tag_cloud.html',
        context_instance=RequestContext(request))

@login_required()
def with_tag(request, tag, sortOrder, object_id=None, page=1):
    query_tag = Tag.objects.get(name=tag)
    tagged_challenges = TaggedItem.objects.get_by_model(models.Challenge, query_tag)
    if sortOrder == "most-recent":
        tagged_challenges = tagged_challenges.order_by('-create_date')
    elif sortOrder == "top-bounty":
        tagged_challenges = tagged_challenges.order_by('-bounty')
    elif sortOrder == "top-votes":
        tagged_challenges = tagged_challenges.order_by('-votes')
    elif sortOrder == "oldest-unsolved":
        tagged_challenges = tagged_challenges.filter(first_completed__isnull=True).order_by('create_date')
    else:
        tagged_challenges = tagged_challenges.filter(sponsor__user__username='tyger-library').order_by('-create_date')
    return render_to_response('challenge/templates/challenges_with_tag.html',
                              dict(tag=tag, tagged_challenges=tagged_challenges, sortOrder=sortOrder),
                              context_instance=RequestContext(request))


#TODO: Hacked multiple views to handle sorting. Should be slicker
class ChallengeListView(ListView):
    context_object_name = "top25_challenge_list"
    model = Challenge
    template_name='challenge/templates/challenge_list.html'
    queryset = Challenge.objects.order_by('-create_date')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListView, self).get_context_data(**kwargs)
        context['sortOrder'] = "most-recent"
        return context

class ChallengeListViewBounty(ListView):
    context_object_name = "top25_challenge_list"
    model = Challenge
    template_name='challenge/templates/challenge_list.html'
    queryset = Challenge.objects.order_by('-bounty')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewBounty, self).get_context_data(**kwargs)
        context['sortOrder'] = "top-bounty"
        return context

class ChallengeListViewVotes(ListView):
    context_object_name = "top25_challenge_list"
    model = Challenge
    template_name='challenge/templates/challenge_list.html'
    queryset = Challenge.objects.order_by('-votes')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewVotes, self).get_context_data(**kwargs)
        context['sortOrder'] = "top-votes"
        return context

class ChallengeListViewOldestUnsolved(ListView):
    context_object_name = "top25_challenge_list"
    model = Challenge
    template_name='challenge/templates/challenge_list.html'
    queryset = Challenge.objects.filter(first_completed__isnull=True).order_by('create_date')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewOldestUnsolved, self).get_context_data(**kwargs)
        context['sortOrder'] = "oldest-unsolved"
        return context

class ChallengeListViewLibrary(ListView):
    context_object_name = "top25_challenge_list"
    model = Challenge
    template_name='challenge/templates/challenge_list.html'
    queryset = Challenge.objects.filter(sponsor__user__username='tyger-library').order_by('-create_date')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewLibrary, self).get_context_data(**kwargs)
        context['sortOrder'] = "tyger-library"
        return context