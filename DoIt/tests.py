from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from DoIt.models import List, Task


def create_user(username, password):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user


def create_list(name, user):
    return List.objects.create(name=name, user=user)


def create_task(name, lit):
    return Task.objects.create(name=name, list=lit)


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
        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User test Added')


class UserLoginTest(TestCase):

    def test_login_successful(self):
        """
        if user exist and the username and password is typed correctly\
        page code should be 200, user should be authenticated and the response\
        should contain 'List of user *username*'
        """
        user = create_user('test', 'ustegenguini')
        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'ustegenguini'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lists of user ' + user.username)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_unsuccessful(self):
        """
        if username or password is incorrect page code should be 200\
        user shouldn't be authenticated, and the message\
        'Please enter a correct username and password. Note that both fields may be case-sensitive'\
        should appear
        """
        user = create_user('test', 'ustegenguini')
        response = self.client.post(reverse('login'), {
            'username': 'tester',
            'password': 'ustegenguini'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Please enter a correct username and password. '
                                      'Note that both fields may be case-sensitive')

        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'ustegengu'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Please enter a correct username and password. '
                                      'Note that both fields may be case-sensitive')


class IndexViewTest(TestCase):

    def test_user_is_not_authenticated(self):
        """
        if any user tries to access the index page without being logged in\
        page should return a 200 code, and a message 'Access Forbidden'
        """
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_no_list_for_user(self):
        """
        if user is logged in and there's no lists for that user, page should\
        return code 200, and a message 'No lists available'
        """
        self.client.force_login(create_user('test', 'super123*secure'))
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [])
        self.assertContains(response, 'No lists available')

    def test_one_list_for_user(self):
        """
        if user is authenticated and there's one list for that user\
        page return code 200, and the name of the list is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        list1 = create_list('list1', user)
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [list1])
        self.assertContains(response, 'list1')

    def test_multiple_list_for_user(self):
        """
        if user is authenticated and there's multiple lists for that user\
        page return code 200, and the name of the lists is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        list1 = create_list('list1', user)
        list2 = create_list('list2', user)
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2])
        self.assertContains(response, 'list1')
        self.assertContains(response, 'list2')

        list3 = create_list('list3', user)
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2, list3])
        self.assertContains(response, 'list1')
        self.assertContains(response, 'list2')
        self.assertContains(response, 'list3')

    def test_delete_list(self):
        """
        if user is authenticated and one list is deleted page return code 200,\
        and the name of the remaining lists is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        list1 = create_list('list1', user)
        list2 = create_list('list2', user)
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2])
        self.assertContains(response, 'list1')
        self.assertContains(response, 'list2')

        List.objects.get(id=list2.id).delete()
        response = self.client.get(reverse('DoIt:index'))
        self.assertSequenceEqual(response.context['list_of_lists'], [list1])
        self.assertContains(response, 'list1')
        self.assertNotContains(response, 'list2')

    def test_edit_list(self):
        """
        if user is authenticated and one list is edited page return code 200,\
        and the name of the updated lists is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        list1 = create_list('list1', user)
        list2 = create_list('list2', user)
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2])
        self.assertContains(response, 'list1')
        self.assertContains(response, 'list2')

        list2.name = 'listupdated'
        list2.save()
        response = self.client.get(reverse('DoIt:index'))
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2])
        self.assertContains(response, 'list1')
        self.assertNotContains(response, 'list2')
        self.assertContains(response, 'listupdated')


class ListTasksViewTest(TestCase):

    def test_user_not_authenticated(self):
        """
        if any user tries to access the list tasks page without being logged in\
        page should return a 200 code, and a message 'Access Forbidden'
        """
        user = create_user('test', 'super123*secure')
        listest = create_list('list', user)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_no_tasks_for_list(self):
        """
        if user is logged in and there's no tasks for that list, page should\
        return code 200, and a message 'No tasks available'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list', user)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_task'], [])
        self.assertContains(response, 'No tasks available')

    def test_one_tasks_for_list(self):
        """
        if user is authenticated and there's one task for that list\
        page return code 200, and the name of the task is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task1 = create_task('task1', listest)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_task'], [task1])
        self.assertContains(response, 'task1')

    def test_multiple_tasks_for_list(self):
        """
        if user is authenticated and there's multiple tasks for that list\
        page return code 200, and the name of the tasks is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task1 = create_task('task1', listest)
        task2 = create_task('task2', listest)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_task'], [task1, task2])
        self.assertContains(response, 'task1')
        self.assertContains(response, 'task2')

    def test_delete_task(self):
        """
        if user is authenticated and one task is deleted\
        page return code 200, and the name of the remaining tasks is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task1 = create_task('task1', listest)
        task2 = create_task('task2', listest)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_task'], [task1, task2])
        self.assertContains(response, 'task1')
        self.assertContains(response, 'task2')

        Task.objects.get(id=task2.id).delete()
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertSequenceEqual(response.context['list_of_task'], [task1])
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')

    def test_edit_task(self):
        """
        if user is authenticated and one task is edited\
        page return code 200, and the name of the edited tasks is shown
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task1 = create_task('task1', listest)
        task2 = create_task('task2', listest)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_task'], [task1, task2])
        self.assertContains(response, 'task1')
        self.assertContains(response, 'task2')

        task2.name = 'taskupdated'
        task2.save()
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertSequenceEqual(response.context['list_of_task'], [task1, task2])
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'taskupdated')

    # add timer with the time to complete all the tasks of the list
