from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from challenge.models import Challenge, Criteria
from django.core.urlresolvers import reverse
from tagging.models import Tag, TaggedItem
import models
from django.contrib.auth.decorators import login_required

#TODO change solution view to list all solutions
#TODO Add view that selects a solution by a specific user.
#TODO: This view should pass the user as well as the challenge we're submitting

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
def with_tag(request, tag, object_id=None, page=1):
    query_tag = Tag.objects.get(name=tag)
    tagged_challenges = TaggedItem.objects.get_by_model(models.Challenge, query_tag)
    tagged_challenges = tagged_challenges.order_by('-create_date')
    return render_to_response('challenge/templates/challenges_with_tag.html',
                              dict(tag=tag, tagged_challenges=tagged_challenges),
                              context_instance=RequestContext(request))
