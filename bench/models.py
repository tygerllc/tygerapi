from django.db import models
from challenge.models import SourceSink, Challenge
from django.contrib.auth.models import User

class CodingRegion(models.Model):
    name = models.CharField(max_length=200)
    sequence = models.CharField(max_length=4000)
    url = models.URLField()
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
    def GenerateSequence(self): #TODO: Add direction
        return self.sequence
    def GeneratePrimer(self): #TODO: Add direction & customize number of bases
        return self.sequence[:20]

class Chassis(CodingRegion): #TODO: Start using chassis
    toxicities = models.ManyToManyField(SourceSink)

class Promoter(CodingRegion):
#    inducedBy = models.ForeignKey(SourceSink)
#    repressedBy = models.ForeignKey(SourceSink)
    PoPS = models.FloatField(default='1.0')

class RBS (CodingRegion):
    RiPS = models.FloatField(default='1.0')

class Protein(CodingRegion):
    proteinOutput = models.ForeignKey(SourceSink)

class Terminator (CodingRegion):
    efficiency = models.FloatField(default='0.98')
    forward = models.BooleanField(default=True) #False for reverse direction

class Bench(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    desc = models.CharField(max_length=2000)
    author = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)
#   promoter/terminator package:
#   protein coding (protein + RBS) package
