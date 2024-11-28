from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project, Task, UserProject, UserTask, Message
import json
from django.urls import reverse

User = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        # Criação de um usuário para testes
        self.user = User.objects.create_user(email="test_user@example.com", password="password", first_name="Test User")
        
        # Criação de um projeto para testes
        self.project = Project.objects.create(name="Projeto Teste", description="Descrição do projeto")
        
        # Criação de uma tarefa para testes
        self.task = Task.objects.create(
            name="Tarefa Teste",
            description="Descrição da tarefa",
            status="pending",
            project=self.project
        )
    
    def test_user_creation(self):
        """Testa a criação de um usuário com email como username."""
        self.assertEqual(self.user.username, "test_user@example.com")
        self.assertEqual(str(self.user), "Test User")
    
    def test_project_creation(self):
        """Testa a criação de um projeto."""
        self.assertEqual(self.project.name, "Projeto Teste")
        self.assertEqual(str(self.project), "Projeto Teste")
    
    def test_task_creation(self):
        """Testa a criação de uma tarefa."""
        self.assertEqual(self.task.name, "Tarefa Teste")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(str(self.task), "Tarefa Teste")


class ViewsTestCase(TestCase):
    def setUp(self):
        # Configura um usuário e loga-o
        self.user = User.objects.create_user(email="test_user@example.com", password="password", first_name="Test User")
        self.client.login(email="test_user@example.com", password="password")
        
        # Criação de um projeto e tarefa para testes
        self.project = Project.objects.create(name="Projeto Teste", description="Descrição do projeto")
        self.task = Task.objects.create(
            name="Tarefa Teste",
            description="Descrição da tarefa",
            status="pending",
            project=self.project
        )
    
    def test_index_view_authenticated(self):
        """Testa a view de index com usuário autenticado."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_project_view(self):
        """Testa a view de detalhes do projeto."""
        response = self.client.get(reverse('project_id', kwargs={'project_id': self.project.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project.html')
        self.assertContains(response, self.project.name)


class TaskUpdateAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test_user@example.com", password="password", first_name="Test User")
        self.client.login(email="test_user@example.com", password="password")
        self.project = Project.objects.create(name="Projeto Teste", description="Descrição do projeto")
        self.task = Task.objects.create(
            name="Tarefa Teste",
            description="Descrição da tarefa",
            status="pending",
            project=self.project
        )
        self.url = reverse('update_task', kwargs={'task_id': self.task.id})
    
    def test_update_task_status(self):
        """Testa a atualização de status da tarefa."""
        payload = {"status": "completed"}
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "completed")


class ChatMessagesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test_user@example.com", password="password", first_name="Test User")
        self.client.login(email="test_user@example.com", password="password")
        self.project = Project.objects.create(name="Projeto Teste", description="Descrição do projeto")
        self.task = Task.objects.create(
            name="Tarefa Teste",
            description="Descrição da tarefa",
            status="pending",
            project=self.project
        )
        self.url = reverse('chat_messages', kwargs={'task_id': self.task.id})
    
    def test_send_message(self):
        """Testa o envio de mensagens no chat."""
        payload = {"content": "Nova mensagem de teste"}
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(task=self.task, content="Nova mensagem de teste").exists())
    
    def test_get_messages(self):
        """Testa a recuperação de mensagens do chat."""
        Message.objects.create(sender=self.user, task=self.task, content="Primeira mensagem")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Primeira mensagem", response.content.decode())
        