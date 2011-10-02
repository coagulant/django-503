# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings
from django.contrib.auth.models import User

from django.test.testcases import TestCase
from django_503 import maintenance
from django_503.models import Config

from tests.views import test_index_page_text


#noinspection PyUnresolvedReferences
class MaintenanceTestCase(TestCase):

    def test_properly_configured(self):
        maintenance_middleware = 'django_503.middleware.MaintenanceMiddleware'
        auth_middleware = 'django.contrib.auth.middleware.AuthenticationMiddleware'

        self.assertIn(maintenance_middleware, settings.MIDDLEWARE_CLASSES,
            msg='Maintenance middleware should be added to MIDDLEWARE_CLASSES in settings.py')
        self.assertIn(auth_middleware, settings.MIDDLEWARE_CLASSES,
            msg='Auth middleware should be added to MIDDLEWARE_CLASSES in settings.py')
        self.assertGreater(settings.MIDDLEWARE_CLASSES.index(maintenance_middleware),
                           settings.MIDDLEWARE_CLASSES.index(auth_middleware),
                           msg='Put maintenance middleware after Auth middleware in MIDDLEWARE_CLASSES')

    def test_maintenance_enable(self):
        Config.objects.create(key='maintenance', value=False)

        # First try, we go in maintenance
        maintenance.enable()
        self.assertTrue(Config.objects.get(key='maintenance').value)

        # Second try, nothing is changed now
        maintenance.enable()
        self.assertTrue(Config.objects.get(key='maintenance').value)

    def test_maintenance_enable_empty_table(self):
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

    def test_maintenance_disable_empty_table(self):
        maintenance.disable()
        self.assertFalse(Config.objects.get(key='maintenance').value)

    def test_maintenance_check(self):
        option = Config.objects.create(key='maintenance', value=False)
        self.assertFalse(maintenance.is_enabled())

        option.value=True
        option.save()
        self.assertTrue(maintenance.is_enabled())


class Maintenance(TestCase):
    
    def test_show_503_index(self):
        response = self.client.get('/')
        self.assertContains(response, test_index_page_text, status_code=200)
        self.assertTemplateNotUsed(response, '503.html')

        maintenance.enable()
        response = self.client.get('/')
        self.assertNotContains(response, test_index_page_text, status_code=503)
        self.assertTemplateUsed(response, '503.html')

    def test_admin_doesnt_see_503(self):
        admin = User.objects.create_superuser('admin', 'admin@foo.bar', 'foobar')
        self.assertTrue(self.client.login(username='admin', password='foobar'))
        
        response = self.client.get('/')
        self.assertContains(response, test_index_page_text)

        maintenance.enable()
        response = self.client.get('/')
        self.assertContains(response, test_index_page_text)

    def test_show_503_redirect(self):
        response = self.client.get('/redirect/', follow=True)
        self.assertRedirects(response, '/', status_code=301)

        maintenance.enable()
        response = self.client.get('/redirect/', follow=True)
        self.assertFalse(response.redirect_chain)
        self.assertTemplateUsed(response, '503.html')