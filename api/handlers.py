from piston.handler import BaseHandler
from piston.utils import rc
from bench.models import Bench
from device.models import Device, Promoter, RBS, Protein, Terminator
from challenge.models import Challenge, Criteria, Environment, SourceSink, UserProfile
from django.contrib.auth.models import User

class CriteriaHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Criteria
    fields = ('desc', 'status',)

class SourceSinkHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = SourceSink

class EnvironmentHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Environment
    fields = ('id', 'name', 'temp', 'pH', ('sources_and_sinks', ()),)

class UserHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = User
    fields = ('username',)

class UserProfileHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = UserProfile
    fields = ('id', ('user', ()),)

class ChallengeHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Challenge
    fields = ('id', 'name', 'tags', 'descrip', 'votes', 'bounty', 'chassis', 'sharing_choice',
              ('environment', ()),
              ('sponsor', ()),
              ('winning_conditions', ()),
        )

    def read(self, request, challenge_id):
        '''
        Returns the challenge specified by challenge_id
        '''
        challenge = Challenge.objects.get(id=challenge_id)
        return challenge

class PromoterHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Promoter
    fields =('id', 'name', 'type', 'sequence', 'external_URL', 'PoPS', ('induced_by', ()), ('repressed_by',()),)

class RBSHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = RBS
    fields =('id', 'name', 'type', 'sequence', 'external_URL', 'RiPS',)

class ProteinHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Protein
    fields =('id', 'name', 'type', 'sequence', 'external_URL', ('protein_output',()),)

class TerminatorHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Terminator
    fields =('id', 'name', 'type', 'sequence', 'external_URL', 'fwd_efficiency', 'rev_efficiency',)

class DeviceHandler (BaseHandler):
    allowed_methods = ('GET',)
    model = Device
    fields = ('id', 'name',
              ('promoter', ()),
              ('rbs', ()),
              ('protein', ()),
              ('terminator', ()),
        )

    def read(self, request, dev_id):
        '''
        Returns the device specified by dev_id
        '''
        dev = Device.objects.get(id=dev_id)
        return dev

    @classmethod
    def sequence_length(self, device):
        length = len(device.promoter.sequence) + len(device.rbs.sequence) + len(device.protein.sequence) + len(device.terminator.sequence)
        return length

class BenchHandler( BaseHandler ):
    allowed_methods = ('GET','DELETE')
    model = Bench
    fields = ('id', 'name', 'desc', 'slug', 'privacy_option',
              ('challenge', ()),
              ('author', ()),
              ('device', ()),
        )

    def read(self, request, slug=None):
        '''
        Returns a list of all benches, or the bench specified by slug
        '''

        base = Bench.objects

        if slug:
            return base.get(slug=slug)
        else:
            return base.all() # Or base.filter(...)

    def delete(self, request, slug):
        '''
        Deletes the bench specified by slug. Returns rc.FORBIDDEN if the request is not generated by the bench's author.
        '''
        b = Bench.objects.get(slug=slug)

        if not request.user == b.author:
            return rc.FORBIDDEN # returns HTTP 401
        b.delete()

        return rc.DELETED # returns HTTP 204

