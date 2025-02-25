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

    def __str__(self):
        return self.email

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Person, on_delete=models.CASCADE, 
                                    related_name="customer_projects")
    employees = models.ManyToManyField(Person, related_name="assigned_projects")

    def __str__(self):
        return str(self.project_id)

class Project_Detail(models.Model):
    project_detail_id = models.AutoField(primary_key=True)
    save_date = models.DateField(auto_now_add=True) # THIS IS PERMANENT WITH AUTO
    image = models.BinaryField(null=False) # Stores image file
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,
                                   related_name="details")