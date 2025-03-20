from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                    related_name="customer_projects")
    employees = models.ManyToManyField(User, related_name="assigned_projects")

    def __str__(self):
        return str(self.project_id)

class Project_Detail(models.Model):
    project_detail_id = models.AutoField(primary_key=True)
    save_date = models.DateField(auto_now_add=True) # THIS IS PERMANENT WITH AUTO
    image = models.BinaryField(null=False) # Stores image file
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,
                                   related_name="details")
    
class Window(models.Model):
    window_id = models.AutoField(primary_key=True)
    # frame = models.ForeignKey(Frame)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    project_detail_id = models.ForeignKey(Project_Detail, on_delete=models.CASCADE, 
                                          related_name="windows")