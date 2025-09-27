from django.db import models
from django.conf import settings

class Service(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    desc = models.TextField()  # краткое описание
    text = models.TextField()  # развёрнутый текст
    inputs = models.CharField(max_length=255)  # значения через запятую
    action_text = models.CharField(max_length=255)

    def get_inputs_list(self):
        return [i.strip() for i in self.inputs.split(',') if i.strip()]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    payout = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image_path = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    
class New(models.Model):
    name = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=1024)
    text = models.TextField()
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    name = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=1024)
    text = models.TextField()
    
    def __str__(self):
        return self.name
    
class Document(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255 * 2)
    
    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='requests'
    )
    description = models.TextField(blank=True, null=True)  # комментарий юзера
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'Новая'),
            ('in_progress', 'В работе'),
            ('done', 'Выполнена')
        ],
        default='new'
    )

    def __str__(self):
        return f"{self.user} → {self.service} ({self.status})"