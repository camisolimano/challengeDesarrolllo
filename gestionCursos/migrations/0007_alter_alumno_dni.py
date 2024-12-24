# Generated by Django 5.1.4 on 2024-12-23 15:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCursos', '0006_alter_inscripcion_curso_alumno_nota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='dni',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
