from django.http import HttpResponse

test_index_page_text = "Sample index page for testing purposes"

def index_page_for_tests(request):
    return HttpResponse(test_index_page_text, mimetype="text/plain")