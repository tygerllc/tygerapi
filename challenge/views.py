from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from challenge.models import Challenge, Criteria
from django.core.urlresolvers import reverse

#TODO change solution view to list all solutions

#TODO Add view that selects a solution by a specific user.

#TODO: This view should pass the user as well as the challenge we're submitting
def submit(request, challenge_id):
    c = get_object_or_404(Challenge, pk=challenge_id)
    try:
        selected_criteria = c.criteria_set.get(pk=request.POST['criteria'])
    except (KeyError, Challenge.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('challenge/detail.html', {
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