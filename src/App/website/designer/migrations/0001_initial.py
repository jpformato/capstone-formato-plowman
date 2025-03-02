# Generated by Django 4.2.19 on 2025-02-25 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=30, null=True)),
                ('password', models.CharField(max_length=50, null=True)),
                ('department', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_projects', to='designer.person')),
                ('employees', models.ManyToManyField(related_name='assigned_projects', to='designer.person')),
            ],
        ),
        migrations.CreateModel(
            name='Project_Detail',
            fields=[
                ('project_detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('save_date', models.DateField(auto_now_add=True)),
                ('image', models.BinaryField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='designer.project')),
            ],
        ),
    ]
