from __future__ import absolute_import

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

from tests.views import index_page_for_tests, plaintext_for_tests


urlpatterns = patterns('',
    url(r'^$', index_page_for_tests),
    url(r'^redirect/$', redirect_to, {'url': '/'}),
    url(r'^plaintext/$', plaintext_for_tests),
)