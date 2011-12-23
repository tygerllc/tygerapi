from piston.handler import BaseHandler
from bench.models import Bench

class BenchHandler( BaseHandler ):
    allowed_methods = ('GET',)
    model = Bench

    def read(self, request, slug=None):
        base = Bench.objects

        if slug:
            return base.get(slug=slug)
        else:
            return base.all() # Or base.filter(...)

