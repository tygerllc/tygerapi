from django.db import models
from challenge.models import SourceSink, UserProfile

PART_CHOICES = (
    ('CHASSIS', 'Chassis'),
    ('PROMOTER', 'Promoter'),
    ('RBS', 'Ribosome binding site'),
    ('PROTEIN', 'Protein'),
    ('TERMINATOR', 'Terminator'),
)

class Part(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=PART_CHOICES, default='PROTEIN')
    sequence = models.CharField(max_length=4000)
    external_URL = models.URLField()
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
    def GenerateSequence(self): #TODO: Add direction
        return self.sequence
    def GeneratePrimer(self): #TODO: Add direction & customize number of bases
        return self.sequence[:20]

class Promoter(Part):
    PoPS = models.FloatField(default='1.0')
    induced_by = models.ForeignKey(SourceSink, blank=True, null=True, related_name='inducers')
    repressed_by = models.ForeignKey(SourceSink, blank=True, null=True, related_name='repressors')

class Protein(Part):
    protein_output = models.ForeignKey(SourceSink, blank=True, null=True)

class Terminator(Part):
    fwd_efficiency = models.FloatField(default='1.0')
    rev_efficiency = models.FloatField(default='1.0')

class RBS(Part):
    RiPS = models.FloatField(default='1.0')

class Device(models.Model):
    name = models.CharField(max_length=200)
    promoter = models.ForeignKey(Promoter)
    rbs = models.ForeignKey(RBS, blank=True, null=True)
    protein = models.ForeignKey(Protein, blank=True, null=True)
    terminator = models.ForeignKey(Terminator)
    owner = models.ForeignKey(UserProfile)
