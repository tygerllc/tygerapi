from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from challenge.models import Challenge
from challenge.forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
from tagging.models import Tag, TaggedItem
from django.views.generic import ListView
import models

def submitEmail(request):
    errors = []
    if request.method == 'POST':
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            try:
                send_mail('New tyger contact',
                request.POST.get('email'),
                'noreply@tyger.us',
                ['togilvie@tyger.us'],
            )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            errors.append("Thanks - we'll keep you up to date!")
            return HttpResponseRedirect('/')
    return render_to_response('index_splash.html',
        {'msg': errors})

def home_view(request):
        return render_to_response('index_splash.html',
        context_instance=RequestContext(request))

@login_required()
def tags(request):
        return render_to_response('challenges_tag_cloud.html',
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
    elif sortOrder == "library":
        tagged_challenges = tagged_challenges.filter(sponsor__user__username='tygerlibrary').order_by('-create_date')
    return render_to_response('challenge_with_tag.html',
                              dict(tag=tag, tagged_challenges=tagged_challenges, sortOrder=sortOrder),
                              context_instance=RequestContext(request))

# Tutorial view looks for all challenges tagged with "tutorial"
@login_required()
def tutorial(request):
    tag = "tutorial"
    tagged_challenges = TaggedItem.objects.get_by_model(models.Challenge, tag)
    tagged_challenges = tagged_challenges.order_by('create_date')
    return render_to_response('challenge_tutorial.html',
                              dict(tag=tag, tagged_challenges=tagged_challenges),
                              context_instance=RequestContext(request))

#TODO: Hacked this into multiple views to handle sorting. Should be slicker
class ChallengeListViewRecent(ListView):
    context_object_name = "top25_challenge_list"
    template_name='challenge_list.html'
    queryset = Challenge.objects.order_by('-create_date')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewRecent, self).get_context_data(**kwargs)
        context['sortOrder'] = "most-recent"
        context['request'] = self.request
        return context

class ChallengeListViewBounty(ListView):
    context_object_name = "top25_challenge_list"
    template_name='challenge_list.html'
    queryset = Challenge.objects.order_by('-bounty')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewBounty, self).get_context_data(**kwargs)
        context['sortOrder'] = "top-bounty"
        context['request'] = self.request
        return context

class ChallengeListViewVotes(ListView):
    context_object_name = "top25_challenge_list"
    template_name='challenge_list.html'
    queryset = Challenge.objects.order_by('-votes')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewVotes, self).get_context_data(**kwargs)
        context['sortOrder'] = "top-votes"
        context['request'] = self.request
        return context

class ChallengeListViewOldestUnsolved(ListView):
    context_object_name = "top25_challenge_list"
    template_name='challenge_list.html'
    queryset = Challenge.objects.filter(first_completed__isnull=True).order_by('create_date')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewOldestUnsolved, self).get_context_data(**kwargs)
        context['sortOrder'] = "oldest-unsolved"
        context['request'] = self.request
        return context

class ChallengeListViewLibrary(ListView):
    context_object_name = "top25_challenge_list"
    template_name='challenge_list.html'
    queryset = Challenge.objects.filter(sponsor__user__username='tyger-library').order_by('-create_date')[:25]

    def get_context_data(self, **kwargs):
        context = super(ChallengeListViewLibrary, self).get_context_data(**kwargs)
        context['sortOrder'] = "library"
        context['request'] = self.request
        return context

@login_required()
def logout_view(request):
    logout(request)
    return redirect('/login/')

def login_view(request):
    state = "Sign In"
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/challenge/')
            else:
                state = "Account is not active, please contact the site admin."
        else:
            state = "Username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username}, context_instance=RequestContext(request))

@login_required()
def about_view(request):
    
        return render_to_response('about.html',context_instance=RequestContext(request))

@login_required()
def contact_view(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']
            sender = form.cleaned_data['sender']
            recipients = ['me@timogilvie.com']
            send_mail(subject, message, name, sender, recipients)
            return HttpResponseRedirect('/thanks/') # Redirect after valid POST
    else:
        form = ContactForm() # Display empty form

    return render_to_response('contact.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required()
def thanks_view(request):
    
        return render_to_response('thanks.html',context_instance=RequestContext(request))
