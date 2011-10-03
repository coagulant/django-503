# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings
from django.contrib.auth.models import User

from django.test.testcases import TestCase
from django_503 import maintenance
from django_503.models import Config

from tests.views import test_index_page_text


#noinspection PyUnresolvedReferences
class BackendTestCase(TestCase):

    def test_properly_configured(self):
        maintenance_middleware = 'django_503.middleware.MaintenanceMiddleware'
        auth_middleware = 'django.contrib.auth.middleware.AuthenticationMiddleware'

        self.assertTrue(maintenance_middleware in settings.MIDDLEWARE_CLASSES,
            msg='Maintenance middleware should be added to MIDDLEWARE_CLASSES in settings.py')
        self.assertTrue(auth_middleware in settings.MIDDLEWARE_CLASSES,
            msg='Auth middleware should be added to MIDDLEWARE_CLASSES in settings.py')
        self.assertTrue((settings.MIDDLEWARE_CLASSES.index(maintenance_middleware) >
                        settings.MIDDLEWARE_CLASSES.index(auth_middleware)),
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

        option.value = True
        option.save()
        self.assertTrue(maintenance.is_enabled())

    def test_maintenance_check_empty_table(self):
        self.assertFalse(maintenance.is_enabled())
        self.assertFalse(Config.objects.get(key='maintenance').value)


class MaintenanceMessageTestCase(TestCase):

    admin_warning = 'Site is on maintenance'

    def create_admin_and_login(self):
        User.objects.create_superuser('admin', 'admin@foo.bar', 'foobar')
        self.assertTrue(self.client.login(username='admin', password='foobar'))

    def test_user_sees_503_error_page_instead_of_index_page(self):
        response = self.client.get('/')
        self.assertContains(response, test_index_page_text, status_code=200)
        self.assertTemplateNotUsed(response, '503.html')

        maintenance.enable()
        response = self.client.get('/')
        self.assertNotContains(response, test_index_page_text, status_code=503)
        self.assertTemplateUsed(response, '503.html')

    def test_user_sees_503_instead_of_redirect(self):
        response = self.client.get('/redirect/', follow=True)
        self.assertRedirects(response, '/', status_code=301)

        maintenance.enable()
        response = self.client.get('/redirect/', follow=True)
        self.assertFalse(response.redirect_chain)
        self.assertTemplateUsed(response, '503.html')

    def test_admin_doesnt_see_503_error_page_instead_of_actual_content(self):
        self.create_admin_and_login()

        response = self.client.get('/')
        self.assertContains(response, test_index_page_text)

        maintenance.enable()
        response = self.client.get('/')
        self.assertContains(response, test_index_page_text)

    def test_admin_sees_warning_in_maintenance_mode_on_html_pages(self):
        admin_warning = 'Site is on maintenance'

        self.create_admin_and_login()
        response = self.client.get('/')
        self.assertNotContains(response, admin_warning)

        maintenance.enable()
        response = self.client.get('/')
        self.assertContains(response, admin_warning)

    def test_no_warnings_for_admin_on_non_html_pages(self):
        admin_warning = 'Site is on maintenance'
        self.create_admin_and_login()
        maintenance.enable()
        response = self.client.get('/plaintext/')
        self.assertNotContains(response, admin_warning)

    def test_user_doesnt_see_warning_in_maintenance_mode(self):
        response = self.client.get('/')
        self.assertNotContains(response, self.admin_warning)

        maintenance.enable()
        response = self.client.get('/')
        self.assertNotContains(response, self.admin_warning, status_code=503)


class MaintenanceAdminTestCase(TestCase):

    def create_admin_and_login(self):
        User.objects.create_superuser('admin', 'admin@foo.bar', 'foobar')
        self.assertTrue(self.client.login(username='admin', password='foobar'))

    def test_admin_accessible(self):
        self.create_admin_and_login()
        response = self.client.get('/admin/django_503/config/')
        self.assertEquals(response.status_code, 200)