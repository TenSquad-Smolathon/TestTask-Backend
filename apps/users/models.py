from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('editor', 'Редактор'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    def is_editor(self):
        return self.role == 'editor'

    def is_admin(self):
        return self.role == 'admin'