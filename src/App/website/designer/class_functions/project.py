from ..models import Project, Person
from .person import read_person

def create_project(attributes):
    """Create a project"""
    customer = read_person(attributes['customer_email'])
    if customer is None:
        return None

    project = Project.objects.create(
        customer = customer
    )

    return project

def read_project(project_id):
    """Read a project from the database"""
    try: 
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None
    
    return project

def update_project(attributes):
    """Update a projects customer or employees"""
    try:
        project = Project.objects.get(project_id=attributes['project_id'])
    except Project.DoesNotExist:
        return None
    
    new_customer = read_person(attributes['customer_email'])
    if new_customer is None:
        return None
    
    project.customer = new_customer
    # for employee in attributes['employees']:
    #     project.employees.add(employee)
    project.employees.set(attributes['employees'])
    project.save()

    return project

def delete_project(project_id):
    """Delete a person in the database by their id"""
    try: 
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return None

    project.delete()
    return True