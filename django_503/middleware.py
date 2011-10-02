from django_503 import maintenance
from django_503.views import view_503

class MaintenanceMiddleware:
    def process_request(self, request):
        if maintenance.is_enabled():
            return view_503(request)
        return

    def process_view(self, request, view_func, view_args, view_kwargs):
        return