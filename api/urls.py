from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import BenchHandler

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

bench_resource = CsrfExemptResource( BenchHandler )

urlpatterns = patterns( '',
    url( r'^bench/(?P<slug>[-_A-Za-z0-9]+)/$', bench_resource, { 'emitter_format': 'json' } ),
    url( r'^bench/$', bench_resource, { 'emitter_format': 'json' } )
)