from django.http import HttpResponse

def call_response(request):
    return HttpResponse(open('comms/calls.xml').read(), content_type='text/xml')
