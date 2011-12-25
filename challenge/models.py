from django.db import models
from tagging.fields import TagField
from tagging.models import Tag
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.URLField()
    active_user = models.BooleanField()
    profile_desc = models.CharField(max_length=500)
    cumulative_votes = models.IntegerField(default=0)
    cumulative_bounty = models.IntegerField(default=0)
    current_votes = models.IntegerField(default=0)
    current_bounty = models.IntegerField(default=0)
#    profile_pic = models.ImageField(default="{{ STATIC_URL }}img/profpic.png")
    
    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

    #TODO add photo to user profile
    #TODO add achievements to user profile
    #TODO Extract User functions to their own app
    #TODO Add function to debit/credit votes & bounties

class SourceSink(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

class Environment(models.Model):
    name = models.CharField(max_length=200)
    temp = models.FloatField(default=37.0)
    pH = models.FloatField(default=7.0)
    sources_and_sinks = models.ManyToManyField(SourceSink)

    def __unicode__(self):
        return self.name

class Challenge(models.Model):
        name = models.CharField(max_length=200)
        slug = models.SlugField(max_length=200)
        descrip = models.CharField(max_length=1000)
        tags = TagField()
        sponsor = models.ForeignKey(UserProfile)
        create_date = models.DateTimeField(editable=False)
        first_completed = models.DateTimeField('First solved', null=True)
        votes = models.IntegerField()
        bounty = models.DecimalField(max_digits = 10, decimal_places=2)
        chassis = models.CharField(max_length=50, default="e coli")
        environment = models.ForeignKey(Environment, default='2')

        def __unicode__(self):
            return self.name
        def bounty_avail(self):
            return not self.first_completed
        def get_tags(self):
            return Tag.objects.get_for_object(self)
#        def save(self):
#            if not self.id:
#                self.create_date = datetime.now()
#                super(Challenge, self).save()


    #TODO: Add type to Criteria [Max bps, No changes to environment, Tyger-Verified]

class Criteria(models.Model):
    challenge = models.ForeignKey(Challenge)
    desc = models.CharField(max_length=200)
    status = models.BooleanField()

    def __unicode__(self):
        return self.desc

class Useful_Link(models.Model):
    challenge = models.ForeignKey(Challenge)
    desc = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.desc

class Useful_Component(models.Model):
    challenge = models.ForeignKey(Challenge)
    desc = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.desc