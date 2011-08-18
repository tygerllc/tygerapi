from django.db import models

class Challenge(models.Model):
        name = models.CharField(max_length=200)
        descrip = models.CharField(max_length=1000)
        points = models.IntegerField()
        bounty = models.DecimalField(max_digits = 10, decimal_places=2)
        create_date = models.DateTimeField('First created')
        first_completed = models.DateTimeField('First solved', null=True)
        def __unicode__(self):
            return self.name
        def bounty_avail(self):
            return not self.first_completed

class Criteria(models.Model):
    challenge = models.ForeignKey(Challenge)
    desc = models.CharField(max_length=200)
    status = models.BooleanField()
    def __unicode__(self):
        return self.desc


