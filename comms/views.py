from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def call_response(request):
    return HttpResponse(open('comms/calls.xml').read(), content_type='text/xml')
