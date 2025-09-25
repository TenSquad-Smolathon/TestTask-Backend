from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    short_desc = models.CharField(max_length=500, verbose_name="Краткое описание")
    desc = models.TextField(verbose_name="Полное описание")
    inputs = models.TextField(
        verbose_name="Поля для ввода (через запятую)",
        help_text="На клиент отдаём как список"
    )
    action_text = models.CharField(max_length=255, verbose_name="Текст кнопки действия")

    def str(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    role = models.CharField(max_length=255, verbose_name="Роль в команде")

    def str(self):
        return f"{self.name} {self.surname} — {self.role}"


class Vacancy(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание")
    requirements = models.TextField(verbose_name="Требования")
    payout = models.CharField(max_length=255, verbose_name="Оплата")

    def str(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название/имя")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Телефон")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    image_path = models.CharField(max_length=500, verbose_name="Путь к изображению")

    def str(self):
        return self.name