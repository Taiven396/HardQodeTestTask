# Generated by Django 5.0.2 on 2024-02-29 15:32

import django.db.models.deletion
import product.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_name_remove_studentsgroup_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='teacher',
            field=models.ForeignKey(limit_choices_to=product.models.teacher_profile_limit_choices_to, on_delete=django.db.models.deletion.PROTECT, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
