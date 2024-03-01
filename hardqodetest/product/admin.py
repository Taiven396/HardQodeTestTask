from django.contrib import admin

from .models import Product, Lesson, StudentsGroup


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'price', 'id']
    search_fields = ['name']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']
    search_fields = ['name', 'product']


@admin.register(StudentsGroup)
class StudentsGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
