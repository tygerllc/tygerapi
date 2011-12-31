from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view
from api.handlers import BenchHandler, DeviceHandler, ChallengeHandler

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

challenge_resource = CsrfExemptResource( ChallengeHandler )
bench_resource = CsrfExemptResource( BenchHandler )
device_resource = CsrfExemptResource( DeviceHandler )

urlpatterns = patterns( '',
    url( r'^challenge/(?P<challenge_id>\d+)/$', challenge_resource, { 'emitter_format': 'json' } ),
    url( r'^device/(?P<dev_id>\d+)/$', device_resource, { 'emitter_format': 'json' } ),
    url( r'^bench/(?P<slug>[-_A-Za-z0-9]+)/$', bench_resource, { 'emitter_format': 'json' } ),
    url( r'^bench/$', bench_resource, { 'emitter_format': 'json' } ),
    url( r'^doc/$', documentation_view),
)