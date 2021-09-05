from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

# Create your tests here.
from django.utils import timezone

from taskManager.forms import CreateTaskForm
from taskManager.models import Task


class taskView(TestCase):

    def test_all_task_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)


class TaskTest(TestCase):

    def create_task(self, title='test title', description='test description'):
        user = User.objects.create(username='admin1', password='admin1234')
        return Task.objects.create(title=title, description=description, created_at=timezone.now(), owner=user)

    def test_task_creation(self):
        task = self.create_task()
        self.assertTrue(isinstance(task, Task))
        self.assertIsNotNone(task)


class formTest(TestCase):

    def task_form_valid_test(self):
        user = User.objects.create(username='admin1', password='admin1234')
        task = Task.objects.create(title='title test', description='description test', created_at=timezone.now(), owner=user)
        data = {'title': task.title, 'description': task.description, }
        form = CreateTaskForm(data=data)
        self.assertTrue(form.is_valid())

    def project_form_invalid_test(self):
        task = Task.objects.create(title='title test', description='')
        data = {'title': task.title, 'description': task.description, }
        form = CreateTaskForm(data=data)
        self.assertTrue(form.is_valid())
