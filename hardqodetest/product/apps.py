from django.apps import AppConfig

from django.core.signals import setting_changed


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        from .signals import set_students_max
        setting_changed.connect(set_students_max)
