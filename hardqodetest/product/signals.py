from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentsGroup


@receiver(post_save, sender=StudentsGroup)
def set_students_max(sender, instance, created, **kwargs):
    if created:
        instance.max_students = instance.product.max_students
        instance.min_students = instance.product.min_students
        instance.save()
    return instance
