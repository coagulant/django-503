from django.template import  Context
from django.template.loader import get_template
import re

from django_503 import maintenance
from django_503.views import view_503


class MaintenanceMiddleware:
    def process_request(self, request):
        if maintenance.is_enabled() and not request.user.is_staff:
            return view_503(request)
        return

    def process_response(self, request, response):
        if maintenance.is_enabled() and request.user.is_staff and self.is_html_response(response):
            template = get_template('maintenance_warning.html')
            warning_message = template.render(Context())
            response.content = re.sub(r'<body.*>', '\g<0>' + warning_message, response.content)
        return response

    def is_html_response(self, response):
        return response['Content-Type'].startswith('text/html')