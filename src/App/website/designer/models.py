from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.name)

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, 
                                    related_name="customer_projects")
    employees = models.ManyToManyField(User, related_name="assigned_projects")
    statuses = models.ManyToManyField(Status, through='ProjectStatus', related_name="projects")
    tracking_number = models.CharField(max_length=36, unique=True, null=True)
    # TEXT AND EMAIL NOTIFICATIONS

    def __str__(self):
        return str(self.project_id)

class ProjectStatus(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('project', 'status', 'start_date')

    def __str__(self):
        return f"{self.project} - {self.status} ({self.start_date} to {self.end_date})"

class Project_Detail(models.Model):
    project_detail_id = models.AutoField(primary_key=True)
    save_date = models.DateField(auto_now_add=True) # THIS IS PERMANENT WITH AUTO
    image = models.BinaryField(null=False) # Stores image file
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                   related_name="details")
    
class Preview(models.Model):
    preview_id = models.AutoField(primary_key=True)
    save_date = models.DateField(auto_now_add=True) # THIS IS PERMANENT WITH AUTO
    detail = models.ForeignKey(Project_Detail, on_delete=models.CASCADE,
                                related_name="previews")

class Window(models.Model):
    window_id = models.AutoField(primary_key=True)
    # frame = models.ForeignKey(Frame)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    preview = models.ForeignKey(Preview, on_delete=models.CASCADE, 
                                          related_name="windows")