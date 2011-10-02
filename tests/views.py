from django.http import HttpResponse

test_index_page_text = "<html><body>Sample index page for testing purposes</body></html>"

def index_page_for_tests(request):
    return HttpResponse(test_index_page_text, mimetype="text/html")

def plaintext_for_tests(request):
    return HttpResponse(test_index_page_text, mimetype="text/plain")