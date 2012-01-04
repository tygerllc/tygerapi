
class ContentTypeMiddleware(object):
    '''
    Custom middleware to make piston respond correctly to PUT and POST requests.
    '''
    def process_request(self, request):
        if request.method in ('POST', 'PUT') and request.META['CONTENT_TYPE'].count(";") > 0:
            request.META['CONTENT_TYPE'] = [c.strip() for c in request.META['CONTENT_TYPE'].split(";") ][0]
        return None