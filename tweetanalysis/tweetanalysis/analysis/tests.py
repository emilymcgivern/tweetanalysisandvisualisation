from django.test import TestCase

from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate

from . import views


class LogInTest(TestCase):

    # login a test user
    def test_login(self):
        c = Client()
        test_user = User.objects.create_user(username='test2', password='test')
        # check that user is signed in
        self.assertTrue(c.login(username='test2', password='test')) 


class SignupPageTests(SimpleTestCase):

    # test that signup page exists and returns status code:
    def test_signup_page_status_code(self):
        response = self.client.get('/signup/')
        self.assertEquals(response.status_code, 200)

    # uses url called correct name:
    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    # uses signup template:
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    # html matches what we've typed:
    def test_signup_page_contains_correct_html(self):
        response = self.client.get('/signup/')
        self.assertContains(response, '<h1>Sign Up</h1>')

    # does not contain incorrect html:
    def test_signup_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/signup/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')


class MonitoringTests(SimpleTestCase):

    # test that selected tweet page exists and returns status code:
    def test_monitoring_page_status_code(self):
        response = self.client.get('/monitoring')
        self.assertEquals(response.status_code, 200)

    # uses url called monitoring (for selected tweet/s):
    def test_view_url_by_name(self):
        response = self.client.get(reverse('monitoring'))
        self.assertEquals(response.status_code, 200)

    # uses desired template:
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('monitoring'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis/monitoring.html')


    # does not contain incorrect html:
    def test_monitoring_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/monitoring')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

class GetUserResultsTests(SimpleTestCase):


    # test that selected tweet page exists and returns status code:
    def test_get_user_results_page_status_code(self):
        response = self.client.get('/get_user_results')
        self.assertEquals(response.status_code, 200)

    # uses url called correct name:
    def test_view_url_by_name(self):
        response = self.client.get(reverse('get_user_results'))
        self.assertEquals(response.status_code, 200)

    # uses desired template:
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('get_user_results'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis/index.html')        # this is where you'll redirect if not logged in

    # html matches what we've typed:
    def test_get_user_results_page_contains_correct_html(self):
        response = self.client.get('/get_user_results')
        self.assertContains(response, '<p>You are not logged in</p>')   # test case not logged in

    # does not contain incorrect html:
    def test_get_user_results_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/get_user_results')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

class IndexTests(SimpleTestCase):

    # def create_user(self):                  
    #     c = Client()
    #     test_user = User.objects.create_user(username='test2', password='test')
    #     c.login(username='test2', password='test')

    # test that selected tweet page exists and returns status code:
    def test_get_index_page_status_code(self):
        response = self.client.get('analysis/index')
        self.assertEquals(response.status_code, 404)            # user not logged in

    # uses url called correct name:
    def test_view_url_by_name(self):
        response = self.client.get(reverse('analysis/index'))
        self.assertEquals(response.status_code, 200)

    # test that selected tweet page exists and returns status code:
    def test_index_page_status_code(self):
        response = self.client.get('analysis/index')
        self.assertEquals(response.status_code, 404)        # user not logged in

    # uses url called correct name:
    def test_view_url_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 302)


class ProfileTests(SimpleTestCase):

    def create_user(self):                  
        self.user = User.objects.create_user(username='testuser', password='ab12345')
        login = self.client.login(username='testuser', password='ab12345')

    # test that selected tweet page exists and returns status code:
    def test_profile_page_status_code(self):
        response = self.client.get('analysis/profile')
        self.assertEquals(response.status_code, 404)            # will be 404 as there are no tweets in test database

