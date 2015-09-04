from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def call_response(request):
    '''
    Returns XML file for Twilio calls. This has
    to be CSRF exempt to accept the Twilio POST request.
    '''

    return HttpResponse(open('comms/calls.xml').read(), content_type='text/xml')
