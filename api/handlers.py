from piston.handler import BaseHandler
from bench.models import Bench
from challenge.models import Challenge, Criteria, Environment, SourceSink

class SourceSinkHandler(BaseHandler):
    model = SourceSink

class EnvironmentHandler(BaseHandler):
    model = Environment
    fields = ('id', 'name', 'temp', 'pH', ('sources_and_sinks', ()))

class ChallengeHandler(BaseHandler):
      model = Challenge
      fields = ('id', 'name', 'tags', 'descrip', 'votes', 'bounty', 'chassis',
                ('environment', ()),
                )

class BenchHandler( BaseHandler ):
    allowed_methods = ('GET',)
    model = Bench
    fields = ('id', 'name', 'desc', 'slug',
              ('challenge', ()),
              ('author', ('id', 'username')),
        )

    def read(self, request, slug=None):
        base = Bench.objects

        if slug:
            return base.get(slug=slug)
        else:
            return base.all() # Or base.filter(...)

