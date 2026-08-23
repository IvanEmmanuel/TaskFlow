from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.tasks.forms import TaskForm, RegisterForm
from django.utils import timezone  

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
        
    def test_user_cannot_access_other_users_task_delete(self):
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
        
    def test_task_search_filter(self):
        Task.objects.create(
            title="Estudiar Django",
            description="Repasar CBV",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        Task.objects.create(
            title="Comprar comida",
            description="Ir al supermercado",
            due_date="2026-08-30",
            status="PENDING",
            priority="LOW",
            user=self.user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            "/tasks/?search=Django"
        )

        self.assertContains(
            response,
            "Estudiar Django"
        )

        self.assertNotContains(
            response,
            "Comprar comida"
        )
        
    def test_task_status_filter(self):
        Task.objects.create(
            title="Tarea pendiente",
            description="Pendiente",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        Task.objects.create(
            title="Tarea completada",
            description="Terminada",
            due_date="2026-08-30",
            status="COMPLETED",
            priority="LOW",
            user=self.user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            "/tasks/?status=COMPLETED"
        )

        self.assertContains(
            response,
            "Tarea completada"
        )

        self.assertNotContains(
            response,
            "Tarea pendiente"
        )
        
    def test_task_priority_filter(self):
        Task.objects.create(
            title="Tarea urgente",
            description="Prioridad alta",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        Task.objects.create(
            title="Tarea normal",
            description="Prioridad baja",
            due_date="2026-08-30",
            status="PENDING",
            priority="LOW",
            user=self.user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            "/tasks/?priority=HIGH"
        )

        self.assertContains(
            response,
            "Tarea urgente"
        )

        self.assertNotContains(
            response,
            "Tarea normal"
        )
        
    def test_task_order_newest(self):
        first_task = Task.objects.create(
            title="Tarea antigua",
            description="Primera tarea",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        second_task = Task.objects.create(
            title="Tarea reciente",
            description="Segunda tarea",
            due_date="2026-08-30",
            status="PENDING",
            priority="LOW",
            user=self.user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get(
            "/tasks/?order=newest"
        )

        tasks = list(response.context["tasks"])

        self.assertEqual(
            tasks[0],
            second_task
        )

        self.assertEqual(
            tasks[1],
            first_task
        )
        
    def test_task_statistics(self):
        Task.objects.create(
            title="Tarea pendiente",
            description="Pendiente",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        Task.objects.create(
            title="Tarea en progreso",
            description="En progreso",
            due_date="2026-08-30",
            status="IN_PROGRESS",
            priority="MEDIUM",
            user=self.user
        )

        Task.objects.create(
            title="Tarea completada",
            description="Completada",
            due_date="2026-08-30",
            status="COMPLETED",
            priority="LOW",
            user=self.user
        )

        Task.objects.create(
            title="Tarea vencida",
            description="Vencida",
            due_date="2026-08-20",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        self.client.login(
            username="Ivan",
            password="123456"
        )

        response = self.client.get("/tasks/")

        self.assertEqual(
            response.context["total_tasks"],
            4
        )

        self.assertEqual(
            response.context["pending_tasks"],
            2
        )

        self.assertEqual(
            response.context["in_progress_tasks"],
            1
        )

        self.assertEqual(
            response.context["completed_tasks"],
            1
        )

        self.assertEqual(
            response.context["overdue_tasks"],
            1
        )
        
    def test_task_priority_label(self):
        task = Task.objects.create(
            title="Tarea importante",
            description="Tarea de prueba",
            due_date="2026-08-30",
            status="PENDING",
            priority="HIGH",
            user=self.user
        )

        self.assertEqual(
            task.priority_label,
            "Prioridad alta: esta tarea requiere atención."
        )
        
    def test_task_status_message(self):
        task = Task.objects.create(
            title="Tarea en progreso",
            description="Tarea de prueba",
            due_date="2026-08-30",
            status="IN_PROGRESS",
            priority="MEDIUM",
            user=self.user
        )

        self.assertEqual(
            task.status_message,
            "Esta tarea está en progreso."
        )
        
    def test_due_date_cannot_be_in_the_past(self):
        form = TaskForm(
            data={
                "title": "Tarea vencida",
                "description": "Tarea de prueba",
                "due_date": "2026-08-20",
                "status": "PENDING",
                "priority": "HIGH",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "due_date",
            form.errors
        )
        
    def test_high_priority_task_cannot_have_due_date_over_30_days(self):
        form = TaskForm(
            data={
                "title": "Tarea urgente",
                "description": "Tarea de prueba",
                "due_date": "2026-10-01",
                "status": "PENDING",
                "priority": "HIGH",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "due_date",
            form.errors
        )
        
    def test_high_priority_task_with_valid_due_date(self):
        form = TaskForm(
            data={
                "title": "Tarea urgente",
                "description": "Tarea de prueba",
                "due_date": "2026-08-30",
                "status": "PENDING",
                "priority": "HIGH",
            }
        )

        self.assertTrue(form.is_valid())
        
    def test_valid_registration_form(self):
        form = RegisterForm(
            data={
                "username": "Carlos",
                "email": "carlos@example.com",
                "password1": "DjangoTest123!",
                "password2": "DjangoTest123!",
            }
        )

        self.assertTrue(form.is_valid())
        
    def test_registration_form_rejects_different_passwords(self):
        form = RegisterForm(
            data={
                "username": "Carlos",
                "email": "carlos@example.com",
                "password1": "DjangoTest123!",
                "password2": "DjangoTest456!",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "password2",
            form.errors
        )
        
    def test_registration_form_rejects_invalid_password(self):
        form = RegisterForm(
            data={
                "username": "Carlos",
                "email": "carlos@example.com",
                "password1": "123",
                "password2": "123",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "password2",
            form.errors
        )