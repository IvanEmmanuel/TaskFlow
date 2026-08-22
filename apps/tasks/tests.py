from django.test import TestCase, Client
from django.contrib.auth.models import User

from apps.tasks.models import Task


class TaskModelTest(TestCase):

    def test_task_belongs_to_user(self):
        user = User.objects.create_user(
            username="Ivan",
            password="123456"
        )

        task = Task.objects.create(
            title="Estudiar Django",
            description="Repasar testing",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=user
        )

        self.assertEqual(task.user, user)
        
        
    def test_task_title_is_saved_correctly(self):
        user = User.objects.create_user(
            username="Ivan",
            password="123456"
        )

        task = Task.objects.create(
            title="Estudiar Django",
            description="Repasar testing",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=user
        )

        self.assertEqual(task.user, user)

        self.assertEqual(
            task.title,
            "Estudiar Django"
        )
        
    def test_task_status_and_priority_are_saved(self):
        user = User.objects.create_user(
            username="Ivan",
            password="123456"
        )

        task = Task.objects.create(
            title="Estudiar Django",
            description="Repasar testing",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=user
        )

        self.assertEqual(task.status, "PENDING")
        self.assertEqual(task.priority, "HIGH")
  


  
class TaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="Ivan",
            password="123456"
        )

    def test_tasks_requires_login(self):
        response = self.client.get("/tasks/")

        self.assertEqual(
            response.status_code,
            302
        )

    def test_authenticated_user_can_access_tasks(self):
        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get("/tasks/")

        self.assertEqual(
            response.status_code,
            200
        )
        
    
    def test_user_only_sees_own_tasks(self):
        other_user = User.objects.create_user(
            username="Carlos",
            password="123456"
        )

        Task.objects.create(
            title="Tarea de Ivan",
            description="Mi tarea",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        Task.objects.create(
            title="Tarea de Carlos",
            description="Tarea de otro usuario",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=other_user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get("/tasks/")

        self.assertContains(
            response,
            "Tarea de Ivan"
        )

        self.assertNotContains(
            response,
            "Tarea de Carlos"
        )
        
    def test_user_cannot_access_other_users_task_detail(self):
        other_user = User.objects.create_user(
            username="Carlos",
            password="123456"
        )

        other_task = Task.objects.create(
            title="Tarea de Carlos",
            description="Tarea privada",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=other_user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            f"/tasks/{other_task.id}/"
        )

        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_user_cannot_edit_other_users_task(self):
        other_user = User.objects.create_user(
            username="Carlos",
            password="123456"
        )

        other_task = Task.objects.create(
            title="Tarea de Carlos",
            description="Tarea privada",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=other_user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            f"/tasks/{other_task.id}/edit/"
        )

        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_user_cannot_delete_other_users_task(self):
        other_user = User.objects.create_user(
            username="Carlos",
            password="123456"
        )

        other_task = Task.objects.create(
            title="Tarea de Carlos",
            description="Tarea privada",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=other_user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            f"/tasks/{other_task.id}/delete/"
        )

        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_user_cannot_modify_other_users_task(self):
        other_user = User.objects.create_user(
            username="Carlos",
            password="123456"
        )

        other_task = Task.objects.create(
            title="Tarea de Carlos",
            description="Tarea privada",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=other_user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.post(
            f"/tasks/{other_task.id}/edit/",
            {
                "title": "Tarea modificada por Ivan",
                "description": "Intento de modificación",
                "due_date": "2026-08-30",
                "status": "PENDING",
                "priority": "HIGH",
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        other_task.refresh_from_db()

        self.assertEqual(
            other_task.title,
            "Tarea de Carlos"
        )
        
    def test_user_cannot_delete_other_users_task(self):
        other_user = User.objects.create_user(
            username="Carlos",
            password="123456"
        )

        other_task = Task.objects.create(
            title="Tarea de Carlos",
            description="Tarea privada",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=other_user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.post(
            f"/tasks/{other_task.id}/delete/"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertTrue(
            Task.objects.filter(
                id=other_task.id
            ).exists()
        )