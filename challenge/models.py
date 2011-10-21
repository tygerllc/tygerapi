from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.URLField()
    active_user = models.BooleanField()
    profile_desc = models.CharField(max_length=500)
    def __unicode__(self):
        return self.user.username
    

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

        def __unicode__(self):
            return self.name
        def bounty_avail(self):
            return not self.first_completed
        def get_tags(self):
            return Tag.objects.get_for_object(self)
        def save(self):
            if not self.id:
                self.create_date = datetime.now()
                super(Challenge, self).save()

class Criteria(models.Model):
    challenge = models.ForeignKey(Challenge)
    desc = models.CharField(max_length=200)
    status = models.BooleanField()
    def __unicode__(self):
        return self.desc


