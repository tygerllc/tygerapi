from piston.handler import BaseHandler
from bench.models import Bench
from device.models import Device, Promoter, RBS, Protein, Terminator
from challenge.models import Challenge, Criteria, Environment, SourceSink, UserProfile
from django.contrib.auth.models import User

class CriteriaHandler(BaseHandler):
    model = Criteria
    fields = ('desc', 'status')

class SourceSinkHandler(BaseHandler):
    model = SourceSink

class EnvironmentHandler(BaseHandler):
    model = Environment
    fields = ('id', 'name', 'temp', 'pH', ('sources_and_sinks', ()))

class UserHandler(BaseHandler):
    model = User
    fields = ('username',)

class UserProfileHandler(BaseHandler):
    model = UserProfile
    fields = ('id', ('user', ()),)

class ChallengeHandler(BaseHandler):
      model = Challenge
      fields = ('id', 'name', 'tags', 'descrip', 'votes', 'bounty', 'chassis', 'sharing_choice',
                ('environment', ()),
                ('sponsor', ()),
                ('winning_conditions', ()),
                )

class PromoterHandler(BaseHandler):
    model = Promoter
    fields =('id', 'name', 'type', 'sequence', 'external_URL', 'PoPS', ('induced_by', ()), ('repressed_by',()),)

class RBSHandler(BaseHandler):
    model = RBS
    fields =('id', 'name', 'type', 'sequence', 'external_URL', 'RiPS')

class ProteinHandler(BaseHandler):
    model = Protein
    fields =('id', 'name', 'type', 'sequence', 'external_URL', ('protein_output',()),)

class TerminatorHandler(BaseHandler):
    model = Terminator
    fields =('id', 'name', 'type', 'sequence', 'external_URL', 'fwd_efficiency', 'rev_efficiency')

class DeviceHandler (BaseHandler):
    model = Device
    fields = ('id', 'name',
              ('promoter', ()),
              ('rbs', ()),
              ('protein', ()),
              ('terminator', ()),
        )

class BenchHandler( BaseHandler ):
    allowed_methods = ('GET','DELETE')
    model = Bench
    fields = ('id', 'name', 'desc', 'slug', 'privacy_option',
              ('challenge', ()),
              ('author', ('id', 'username')),
              ('device', ()),
        )

    def read(self, request, slug=None):
        base = Bench.objects

        if slug:
            return base.get(slug=slug)
        else:
            return base.all() # Or base.filter(...)

    def delete(self, request, slug):
        b = Bench.objects.get(slug=slug)

        if not request.user == b.author:
            return rc.FORBIDDEN # returns HTTP 401

        b.delete()

        return rc.DELETED # returns HTTP 204