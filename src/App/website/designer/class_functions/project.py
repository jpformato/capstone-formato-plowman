from ..models import Project, Customer, Status, ProjectStatus
from .customer import read_customer_email, create_customer
from django.contrib.auth.models import User
import uuid

# Contract, Final Measure, Order, ETA, Installation, <-- Upon the completion of installation marks the completion of the project
statuses = ['Contract', 'Final Measure', 'Order', 'ETA', 'Installation']

def create_project(customer_email, employee_id):
    """Create a project"""
    print (employee_id)
    customer = read_customer_email(customer_email)
    if customer is None:
        print(customer_email)
        customer = create_customer(email=customer_email)
        if customer is None:
            print("in 2nd if")
            return None
    
    try:
        employee = User.objects.get(id=employee_id)
    except User.DoesNotExist:
        return None

    project = Project.objects.create(customer = customer)
    project.employees.add(employee)
    return project

def read_project(project_id):
    """Read a project from the database"""
    try: 
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None
    
    return project

def read_project_tracking(tracking_number):
    try: 
        project = Project.objects.get(tracking_number=tracking_number)
    except Project.DoesNotExist:
        return None
    
    return project

def update_project(project_id, customer_email=None, employees=None):
    """Update a projects customer or employees"""
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None
    
    if customer_email is not None:
        new_customer = read_customer_email(customer_email)
        if new_customer is None:
            return None
        project.customer = new_customer
        project.save()

    if employees is not None:
        for employee_email in employees:
            new_employee = User.objects.get(email=employee_email)
            if new_employee is not None:
                project.employees.add(new_employee)

    return project

def add_employee(project_id, employee_email):
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None
    
    new_employee = User.objects.get(email=employee_email)
    if new_employee is None:
        return None
    
    project.employees.add(new_employee)
    return project

def delete_project(project_id):
    """Delete a person in the database by their id"""
    try: 
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None

    project.delete()
    return True

def generate_tracking_number():
    while True:
        tracking_number = uuid.uuid4()
        if not Project.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number

# set connection to statuses and generate tracking number
def start_project(project_id):
    try: 
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None
    
    if project.statuses.count() > 0 and project.statuses.count() < 5:
        project.statuses.clear()
    
    for status in statuses:
        status = Status.objects.get(name=status)
        project.statuses.add(status)

    project.tracking_number = generate_tracking_number()
    project.save()
    
    return project