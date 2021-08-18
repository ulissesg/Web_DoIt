from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


def create_user(username, password):
    return User.objects.create(username=username, password=password)


class UserSignUpTest(TestCase):

    def test_field_required(self):
        """
        if user tries to create a user with a required field empty,\
        page should return status code 200 and 'This field is required'
        """
        response = self.client.post(reverse('DoIt:signup'), {
            'username': '',
            'password': '123456789',
            'password2': '123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': '',
            'password2': '123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': '123456789',
            'password2': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': '',
            'password': '',
            'password2': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    def test_password_all_numeric(self):
        """
        if user tries to create a user with all numeric password,\
        page should return status code 200 and 'This password is entirely numeric'
        """
        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': '123456789',
            'password2': '123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is entirely numeric')

    def test_password_less_than_8_characters(self):
        """
        if user tries to create a user with a password that contains less than 8 characters,\
        page should return status code 200 and 'This password is too short. It must contain at least 8 characters.'
        """
        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': 'user',
            'password2': 'user'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': 'usterst',
            'password2': 'usterst'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')

    def test_password_too_similar_to_personal_info(self):
        """
        if user tries to create a user with a password that's too similar to the given personal\
        info page should return status code 200 and 'The password is too similar to the *similar field*'
        """
        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'testcase',
            'password': 'testcase',
            'password2': 'testcase'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password is too similar to the username')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'lucifer',
            'first_name': 'testuser',
            'password': 'testuser',
            'password2': 'testuser'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password is too similar to the first name')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'lucifer',
            'first_name': 'lucifer',
            'last_name': 'testuser',
            'password': 'testuser',
            'password2': 'testuser'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password is too similar to the last name')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'lucifer',
            'first_name': 'lucifer',
            'last_name': 'morningstar',
            'email': 'testuser@gmail.com',
            'password': 'testuser',
            'password2': 'testuser'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password is too similar to the email')

    def test_password_too_common(self):
        """
        if user tries to create a user with a password that's too common,\
        page should return status code 200 and 'This password is too common.'
        """
        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too common')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': 'user',
            'password2': 'user'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too common')

        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': '12345',
            'password2': '12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too common')

    def test_user_already_exist(self):
        """
        If user already exist page should return status code 200 and the message\
        'A user with that username already exists.'
        """
        create_user('test', 'super123*secure')
        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password': 'super123*secure',
            'password2': 'super123*secure'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists.')

    def test_user_added_successfully(self):
        """
        If user is added successfully page should return code 302 user is \
        redirected to login page, and message 'User *username* added' appears
        """
        response = self.client.post(reverse('DoIt:signup'), {
            'username': 'test',
            'password1': 'super123*secure',
            'password2': 'super123*secure'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User test Added')
