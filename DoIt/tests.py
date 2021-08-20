from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.http import Http404
from django.shortcuts import get_object_or_404
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


def create_task(name, lit, time=None, is_important=None, is_done=None):
    return Task.objects.create(name=name, list=lit, time_it_takes=time, is_done=is_done,
                               is_important=is_important)


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


class IndexTest(TestCase):

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
        self.assertContains(response, str(list1.name))

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
        self.assertContains(response, str(list1.name))
        self.assertContains(response, str(list2.name))

        list3 = create_list('list3', user)
        response = self.client.get(reverse('DoIt:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2, list3])
        self.assertContains(response, str(list1.name))
        self.assertContains(response, str(list2.name))
        self.assertContains(response, str(list3.name))

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
        self.assertContains(response, str(list1.name))
        self.assertContains(response, str(list2.name))

        List.objects.get(id=list2.id).delete()
        response = self.client.get(reverse('DoIt:index'))
        self.assertSequenceEqual(response.context['list_of_lists'], [list1])
        self.assertContains(response, str(list1.name))
        self.assertNotContains(response, str(list2.name))

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
        self.assertContains(response, str(list1.name))
        self.assertContains(response, str(list2.name))

        list2.name = 'listupdated'
        list2.save()
        response = self.client.get(reverse('DoIt:index'))
        self.assertSequenceEqual(response.context['list_of_lists'], [list1, list2])
        self.assertContains(response, str(list1.name))
        self.assertNotContains(response, 'list2')
        self.assertContains(response, str(list2.name))


class ListTasksTest(TestCase):

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
        self.assertContains(response, str(task1.name))

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
        self.assertContains(response, str(task1.name))
        self.assertContains(response, str(task2.name))

        task3 = create_task('task3', listest)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertSequenceEqual(response.context['list_of_task'], [task1, task2, task3])
        self.assertContains(response, str(task1.name))
        self.assertContains(response, str(task2.name))
        self.assertContains(response, str(task3.name))

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
        self.assertContains(response, str(task1.name))
        self.assertContains(response, str(task2.name))

        Task.objects.get(id=task2.id).delete()
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertSequenceEqual(response.context['list_of_task'], [task1])
        self.assertContains(response, str(task1.name))
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
        self.assertContains(response, str(task1.name))
        self.assertContains(response, str(task2.name))

        task2.name = 'taskupdated'
        task2.save()
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertSequenceEqual(response.context['list_of_task'], [task1, task2])
        self.assertContains(response, str(task1.name))
        self.assertNotContains(response, 'task2')
        self.assertContains(response, str(task2.name))

    def test_total_minutes_clock(self):
        """
        Test the sum of all the minutes to conclude all tasks of one list that \
        aren't done, page returns the sum in minutes of all tasks
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task1 = create_task('task1', listest, 20, is_done=True)
        task2 = create_task('task2', listest, 45, is_done=True)
        task3 = create_task('task3', listest, 1000)
        task4 = create_task('task4', listest, 350)
        time_finish_list = task3.time_it_takes + task4.time_it_takes
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Remaining time to finish all tasks of the list is : '
                            + str(time_finish_list) + ' minutes')
        self.assertEqual(response.context['time_finish_list'], time_finish_list)

    def test_ordering_tasks_of_list_by_importance(self):
        """
        if user is authenticated and there's multiple tasks for that list\
        page return code 200, and the name of the tasks is shown ordered by importance
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task1 = create_task('task1', listest)
        task2 = create_task('task2', listest)
        task3 = create_task('task3', listest, is_important=True)
        task4 = create_task('task4', listest)
        task5 = create_task('task5', listest, is_important= True)
        response = self.client.get(reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertSequenceEqual(response.context['list_of_task'], [task3, task5, task1, task2, task4])
        self.assertContains(response, str(task1.name))
        self.assertContains(response, str(task2.name))
        self.assertContains(response, str(task3.name))
        self.assertContains(response, str(task4.name))
        self.assertContains(response, str(task5.name))


class NewListTest(TestCase):

    def test_user_not_authenticated(self):
        """
        If user isn't authenticated page returns code 200 and the message\
        'Access Forbidden'
        """
        create_user('test', 'super123*secure')
        response = self.client.get(reverse('DoIt:new_list'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_list_name_empty(self):
        """
        if user doesn't type anything in the name field \
        page returns code 200 and the message 'This field is required'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        response = self.client.post(reverse('DoIt:new_list'), {
            'name': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'This field is required')

    def test_list_added_successfully(self):
        """
        if name field isn't empty page returns code 302 \
        redirects to index and displays the message 'List *name* created successfully'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        response = self.client.post(reverse('DoIt:new_list'), {
            'name': 'test'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('DoIt:index'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'List test created successfully')


class EditListTest(TestCase):

    def test_user_not_authenticated(self):
        """
        if any user tries to edit a list without being logged in\
        page should return a 200 code, and a message 'Access Forbidden'
        """
        user = create_user('test', 'super123*secure')
        listest = create_list('list', user)
        response = self.client.get(reverse('DoIt:list_edit', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_load_list_info_on_form(self):
        """
        test if all info are correctly loaded into the edit page
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        response = self.client.get(reverse('DoIt:list_edit', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['object'], listest)
        self.assertContains(response, ' value="' + str(listest.name) + '"')
        self.assertContains(response, 'selected>' + str(listest.user))


class DeleteListTest(TestCase):

    def test_user_not_authenticated(self):
        """
        if any user tries to delete a list without being logged in\
        page should return a 200 code, and a message 'Access Forbidden'
        """
        user = create_user('test', 'super123*secure')
        listest = create_list('list', user)
        response = self.client.get(reverse('DoIt:list_delete', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_confirm_delete(self):
        """
        if confirm works, page returns index page, with message\
        'List *name*  deleted successfully'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        response = self.client.post(reverse('DoIt:list_delete', kwargs={'pk': listest.id}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('DoIt:index'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'List ' + str(listest.name) + ' deleted successfully')


class NewTaskTest(TestCase):

    def test_user_not_authenticated(self):
        """
        If user isn't authenticated page returns code 200 and the message\
        'Access Forbidden'
        """
        user = create_user('test', 'super123*secure')
        listest = create_list('list1', user)
        response = self.client.get(reverse('DoIt:new_task', kwargs={'pk': listest.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_task_name_empty(self):
        """
        if user doesn't type anything in the name field \
        page returns code 200 and the message 'This field is required'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        response = self.client.post(reverse('DoIt:new_task', kwargs={'pk': listest.id}), {
            'name': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'This field is required')

    def test_task_added_successfully(self):
        """
        if name field isn't empty page returns code 302 \
        redirects to list tasks and displays the message 'task *name* created successfully'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        response = self.client.post(reverse('DoIt:new_task', kwargs={'pk': listest.id}), {
            'name': 'test'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Task test created successfully')

        response = self.client.post(reverse('DoIt:new_task', kwargs={'pk': listest.id}), {
            'name': 'test2',
            'description': 'description test',
            'is_done': 'Yes',
            'start_date': '01/14/1987',
            'end_date': '08/20/2021',
            'time_it_takes': '5',
            'is_important': 'No'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertNotEqual(get_object_or_404(Task, name='test2'), Http404)
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Task test2 created successfully')


class EditTaskTest(TestCase):

    def test_user_not_authenticated(self):
        """
        if any user tries to edit a task without being logged in\
        page should return a 200 code, and a message 'Access Forbidden'
        """
        user = create_user('test', 'super123*secure')
        listest = create_list('list', user)
        task = create_task('test1', listest)
        response = self.client.get(reverse('DoIt:task_edit', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_load_list_info_on_form(self):
        """
        test if info are correctly loaded into the edit page
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task = create_task('test1', listest)
        response = self.client.get(reverse('DoIt:task_edit', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['object'], task)
        self.assertContains(response, ' value="' + str(task.name) + '"')
        self.assertEqual(response.context['list'], listest)


class DeleteTaskTest(TestCase):

    def test_user_not_authenticated(self):
        """
        if any user tries to delete a task without being logged in\
        page should return a 200 code, and a message 'Access Forbidden'
        """
        user = create_user('test', 'super123*secure')
        listest = create_list('list', user)
        task = create_task('test1', listest)
        response = self.client.get(reverse('DoIt:task_delete', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Access Forbidden')

    def test_confirm_delete(self):
        """
        if confirm works, page returns list tasks page, with message\
        'Task *name* deleted successfully'
        """
        user = create_user('test', 'super123*secure')
        self.client.force_login(user)
        listest = create_list('list1', user)
        task = create_task('test1', listest)
        response = self.client.post(reverse('DoIt:task_delete', kwargs={'pk': task.id}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('DoIt:tasks', kwargs={'pk': listest.id}))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Task ' + str(task.name) + ' deleted successfully')
