# Generated by Django 5.1.4 on 2024-12-21 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCursos', '0003_alter_curso_codigo_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='codigo_curso',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
