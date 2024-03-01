# Generated by Django 5.0.2 on 2024-02-29 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='product.product'),
        ),
        migrations.AlterField(
            model_name='studentsgroup',
            name='max_students',
            field=models.PositiveIntegerField(default=0),
        ),
    ]