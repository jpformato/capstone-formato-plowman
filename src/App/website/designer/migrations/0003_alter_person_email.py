# Generated by Django 5.1.6 on 2025-02-11 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0002_alter_person_department_alter_person_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
