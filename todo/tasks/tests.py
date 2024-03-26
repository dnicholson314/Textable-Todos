from django.test import TestCase
from django.urls import reverse
from .models import Task

# Create your tests here.
class TaskFormTests(TestCase):

    def test_create_task_form(self):
        """
        Tests all the functionality surrounding creating tasks: whether the task is created properly, whether it has the proper default attributes, and whether the app redirects the user to the proper page.
        """

        url = reverse("list")

        data = {
              'title': "Test Task"
        }

        response = self.client.post(url, data)

        # Test 1: The task was created
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.first()

        # Test 2: The task has the proper attributes
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.complete)
        self.assertEqual(task.description, "")

        # Test 3: Confirm redirect back to main page
        self.assertRedirects(response, "/")

    def test_update_task_form(self):
        """
        Tests all the functionality surrounding updating tasks: whether the tasks are updated to the desired attributes and whether the app redirects the user to the proper page.
        """

        old_task = Task.objects.create(
            title="Test Task"
        )
        url = reverse(f"update_task", args=[old_task.id])

        # Test 1: Confirm correctly updates attributes
        new_title = "Another Test Task"
        new_complete = True
        new_description = 'Test description'

        data = {
            'title': new_title,
            'complete': new_complete,
            'description': new_description,
        }
        response = self.client.post(url, data)

        new_task = Task.objects.first()
        self.assertEqual(new_task.title, new_title)
        self.assertTrue(new_task.complete, new_complete)
        self.assertEqual(new_task.description, new_description)

        # Test 2: Confirm redirect back to main page
        self.assertRedirects(response, "/")

    def test_delete_task_form(self):
        """
        Tests whether the delete task form deletes the task and redirects the user to the proper page.
        """

        task = Task.objects.create(
            title='Test Task'
        )
        url = reverse(f"delete_task", args=[task.id])

        # Test 1: Confirm correctly deletes task
        response = self.client.post(url)
        self.assertEqual(Task.objects.count(), 0)

        # Test 2: Confirm redirect back to main page
        self.assertRedirects(response, "/")