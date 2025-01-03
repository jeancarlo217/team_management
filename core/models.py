from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from stdimage.models import StdImageField

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O campo de e-mail é obrigatório!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ser is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ser is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    TIPO_CHOICES = [
        ('funcionario', 'Funcionário'),
        ('super', 'Gerente'),
    ]
    perfil = StdImageField(
        upload_to='perfil/',
        delete_orphans=True,
        blank=True,
        variations={'thumb': {'width': 50, 'height': 50, 'crop': True}}
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='DEV')
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Membros da Equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def save(self, *args, **kwargs):
        if not self.username:  # Apenas define o username se ele estiver vazio
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name
    
    objects = UserManager()


class Project(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True, max_length=25)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('', ''),
        ('pending', 'Pendente'),
        ('in_progress', 'Em Progresso'),
        ('completed', 'Concluída'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    deadline = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserProject(models.Model):
    up_user = models.ForeignKey(User, on_delete=models.CASCADE)
    up_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.up_user.first_name} - {self.up_project.name}"
    

class UserTask(models.Model):
    ut_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ut_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ut_user.first_name} - {self.ut_task.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp}"
