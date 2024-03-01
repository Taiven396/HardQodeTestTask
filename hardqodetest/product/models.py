from django.db import models
from django.contrib.auth.models import User



def teacher_profile_limit_choices_to():
    return {'profile__status': 'Учитель'}


class Product(models.Model):
    """
    Модель продукта.

    Параметры:
        name: Название продукта
        teacher: Автор/преподаватель продукта
        start: Дата и время старта
        price: Стоимость продукта
        students: Студенты у которых есть доступ к продукту
    """
    name = models.CharField(max_length=128, unique=True)
    teacher = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='teacher', limit_choices_to=teacher_profile_limit_choices_to)
    start = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_students = models.PositiveIntegerField(default=30)
    min_students = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Lesson(models.Model):
    """
    Модель урока

    Параметры:
        name: Название урока
        link: Ссылка на видео
        product: К какому продукту относится урок
    """
    name = models.CharField(max_length=128, unique=True)
    link = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='lessons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class StudentsGroup(models.Model):
    """
    Модель группы студентов

    Параметры:
        name: Название группы
        students: Студенты
        product: Продукт к которому относится группа

    """
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(User, related_name='members', blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='groups')
    max_students = models.PositiveIntegerField(default=0)
    min_students = models.PositiveIntegerField(default=0)
    current_students = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа студентов'
        verbose_name_plural = 'Группы студентов'



