from django.test import TestCase
from django.urls import reverse
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

USERNAME1 = 'testuser'
USERNAME2 = 'testuser2'
PASSWORD = '12345'
CREATE_URL = reverse("list")

class UserTestCases(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username=USERNAME1, password=PASSWORD)
        self.user2 = User.objects.create_user(username=USERNAME2, password=PASSWORD)
        self.user1_task = Task.objects.create(
            title = "Test Task",
            user = self.user1
        )

    def test_create_user(self):
        """
        Tests whether users are properly created.
        """
        user_count = User.objects.filter(username=USERNAME1).count()
        self.assertEqual(user_count, 1)

    def test_login_user(self):
        """
        Tests whether users can login to the website.
        """
        logged_in = self.client.login(username=USERNAME1, password=PASSWORD)
        self.assertTrue(logged_in)

    def test_logged_out_user_main_page_access(self):
        """
        Tests that users that are not logged in cannot access the main page.
        """
        response = self.client.get(CREATE_URL)
        self.assertNotEqual(response.url, CREATE_URL)

    def test_logged_out_user_update_page_access(self):
        """
        Tests that users that are not logged in cannot access the update task form.
        """
        update_url = reverse("update_task", args=[self.user1_task.id])
        redirect_url = f"/login/?next={update_url}"
        response = self.client.get(update_url)
        self.assertRedirects(response, redirect_url)

    def test_logged_out_user_delete_page_access(self):
        """
        Tests that users that are not logged in cannot access the delete task form.
        """
        delete_url = reverse("delete_task", args=[self.user1_task.id])
        redirect_url = f"/login/?next={delete_url}"
        response = self.client.get(delete_url)
        self.assertRedirects(response, redirect_url)

    def test_wrong_user_update_page_access(self):
        """
        Tests whether users can update tasks that are not their own.
        """
        self.client.login(username=USERNAME2, password=PASSWORD)

        update_url = reverse("update_task", args=[self.user1_task.id])
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 403)

    def test_wrong_user_delete_page_access(self):
        self.client.login(username=USERNAME2, password=PASSWORD)

        delete_url = reverse("delete_task", args=[self.user1_task.id])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 403)

class TaskTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME1, password=PASSWORD)
        self.client.login(username=USERNAME1, password=PASSWORD)

    def test_create_task(self):
        """
        Tests all the functionality surrounding creating tasks: whether the task is created properly, whether it has the proper default attributes, and whether the app redirects the user to the proper page.
        """
        data = {
              'title': "Test Task",
        }

        response = self.client.post(CREATE_URL, data)

        # Test 1: The task was created
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()

        # Test 2: The task has the proper attributes
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.complete)
        self.assertEqual(task.description, "")

        # Test 3: Confirm redirect back to main page
        self.assertRedirects(response, CREATE_URL)

    def test_update_task(self):
        """
        Tests all the functionality surrounding updating tasks: whether the tasks are updated to the desired attributes and whether the app redirects the user to the proper page.
        """

        old_task = Task.objects.create(
            title="Test Task",
            user=self.user
        )
        update_url = reverse(f"update_task", args=[old_task.id])

        # Test 1: Confirm correctly updates attributes
        new_title = "Another Test Task"
        new_complete = True
        new_description = 'Test description'

        data = {
            'title': new_title,
            'complete': new_complete,
            'description': new_description,
        }
        response = self.client.post(update_url, data)

        new_task = Task.objects.first()
        self.assertEqual(new_task.title, new_title)
        self.assertTrue(new_task.complete, new_complete)
        self.assertEqual(new_task.description, new_description)

        # Test 2: Confirm redirect back to main page
        self.assertRedirects(response, CREATE_URL)

    def test_delete_task(self):
        """
        Tests whether the delete task form deletes the task and redirects the user to the proper page.
        """

        task = Task.objects.create(
            title='Test Task',
            user=self.user,
        )
        url = reverse(f"delete_task", args=[task.id])

        # Test 1: Confirm correctly deletes task
        response = self.client.post(url)
        self.assertEqual(Task.objects.count(), 0)

        # Test 2: Confirm redirect back to main page
        self.assertRedirects(response, CREATE_URL)