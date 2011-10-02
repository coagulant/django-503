# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings

from django.test.testcases import TestCase
from django_503 import maintenance
from django_503.models import Config

from tests.views import test_index_page_text


#noinspection PyUnresolvedReferences
class MaintenanceTestCase(TestCase):

    def test_properly_configured(self):
        self.assertIn('django_503.middleware.MaintenanceMiddleware', settings.MIDDLEWARE_CLASSES,
            msg='Maintenance middleware should be added to MIDDLEWARE_CLASSES in settings.py')

    def test_maintenance_enable(self):
        Config.objects.create(key='maintenance', value=False)

        # First try, we go in maintenance
        maintenance.enable()
        self.assertTrue(Config.objects.get(key='maintenance').value)

        # Second try, nothing is changed now
        maintenance.enable()
        self.assertTrue(Config.objects.get(key='maintenance').value)

    def test_maintenance_disable(self):
        Config.objects.create(key='maintenance', value=True)

        # First try, turn off maintenance mode
        maintenance.disable()
        self.assertFalse(Config.objects.get(key='maintenance').value)

        # Second try, nothing is changed now
        maintenance.disable()
        self.assertFalse(Config.objects.get(key='maintenance').value)

    def test_maintenance_check(self):
        option = Config.objects.create(key='maintenance', value=False)
        self.assertFalse(maintenance.is_enabled())

        option.value=True
        option.save()
        self.assertTrue(maintenance.is_enabled())


class Maintenance(TestCase):
    
    def test_show_503(self):
        response = self.client.get('/')
        self.assertContains(response, test_index_page_text, status_code=200)
        self.assertTemplateNotUsed(response, '503.html')

        maintenance.enable()
        response = self.client.get('/')
        self.assertNotContains(response, test_index_page_text, status_code=503)
        self.assertTemplateUsed(response, '503.html')