from django.http import HttpResponse
from django.template import loader

def view_503(request):
    return HttpResponse(loader.render_to_string('503.html'), status=503)