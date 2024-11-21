# Generated by Django 5.1.2 on 2024-11-18 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentclass',
            name='form_tutor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_class_tutor', to='journal.teacher'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
