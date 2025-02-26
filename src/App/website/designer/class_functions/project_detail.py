from ..models import Project_Detail
from .project import read_project

def create_project_detail(attributes):
    image = attributes['image']
    project_id = attributes['project_id']
    
    project = read_project(project_id)
    if project is None:
        return None

    project_detail = Project_Detail.objects.create(
        image = image,
        project_id = project
    )

    return project_detail

def read_project_detail(project_detail_id):
    try:
        project_detail = Project_Detail.objects.get(project_detail_id=project_detail_id)
    except Project_Detail.DoesNotExist:
        return None
    
    return project_detail

def update_project_detail(attributes):
    try:
        project_detail = Project_Detail.objects.get(project_detail_id=attributes['project_detail_id'])
    except Project_Detail.DoesNotExist:
        return None

    project_detail.image = attributes['image']
    project_detail.project_id = attributes['project_id']
    project_detail.save()
    
    return project_detail


def delete_project_detail(project_detail_id):
    try:
        project_detail = Project_Detail.objects.get(project_detail_id=project_detail_id)
    except Project_Detail.DoesNotExist:
        return False
    
    project_detail.delete()
    return True