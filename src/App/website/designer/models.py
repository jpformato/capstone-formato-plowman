from django.db import models

# Create your models here.

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=50, null=True)
    department = models.CharField(max_length=30, null=True)