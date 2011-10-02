from __future__ import absolute_import
from django.conf.urls.defaults import patterns, url
from tests.views import index_page_for_tests


urlpatterns = patterns('',
    url('^$', index_page_for_tests)
)