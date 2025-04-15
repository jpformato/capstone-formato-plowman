# Generated by Django 5.1.6 on 2025-04-15 20:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('frame_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.BinaryField(null=True)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('tracking_number', models.CharField(max_length=36, null=True, unique=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_projects', to='designer.customer')),
                ('employees', models.ManyToManyField(related_name='assigned_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project_Detail',
            fields=[
                ('project_detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('save_date', models.DateField(auto_now_add=True)),
                ('image', models.BinaryField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='designer.project')),
            ],
        ),
        migrations.CreateModel(
            name='Preview',
            fields=[
                ('preview_id', models.AutoField(primary_key=True, serialize=False)),
                ('save_date', models.DateField(auto_now_add=True)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previews', to='designer.project_detail')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='designer.project')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='designer.status')),
            ],
            options={
                'unique_together': {('project', 'status', 'start_date')},
            },
        ),
        migrations.AddField(
            model_name='project',
            name='statuses',
            field=models.ManyToManyField(related_name='projects', through='designer.ProjectStatus', to='designer.status'),
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('window_id', models.AutoField(primary_key=True, serialize=False)),
                ('x1', models.IntegerField()),
                ('y1', models.IntegerField()),
                ('x2', models.IntegerField()),
                ('y2', models.IntegerField()),
                ('frame', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='windows', to='designer.frame')),
                ('preview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='windows', to='designer.preview')),
            ],
        ),
    ]
