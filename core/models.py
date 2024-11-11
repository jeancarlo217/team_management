from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from stdimage.models import StdImageField

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,  email, password, **extra_fields):

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
        ('FUNC_V2', 'Funcionário V2'),
        ('FUNC_VV', 'Funcionário VV'),
        ('CLI_V2', 'Cliente V2'),
        ('DEV', 'Desenvolvimento'),
    ]
    perfil =  StdImageField(
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

    def __str__(self):
        return self.email
    
    objects = UserManager()


class Base(models.Model):
    created = models.DateField('Creation', auto_now_add=True)
    modified = models.DateField('Update', auto_now=True)
    active = models.BooleanField('Active?', default=True)

    class Meta:
        abstract = True