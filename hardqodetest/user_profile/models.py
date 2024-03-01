from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    """
    Модель профиля пользователя

    Параметры:
        user: Сущность User
        status: В каком статсуе пользователь ученик/учитель/новый пользователь
    """
    status_choice = [
        ('Студент', 'Студент'),
        ('Учитель', 'Учитель'),
        ('Новый', 'Новый')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    status = models.CharField(max_length=10, choices=status_choice)

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'
