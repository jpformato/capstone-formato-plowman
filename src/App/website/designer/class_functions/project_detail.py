from ..models import Project_Detail
from .project import read_project

def create_project_detail(image, project_id):
    project = read_project(project_id)
    if project is None:
        return None

    project_detail = Project_Detail.objects.create(
        image = image,
        project = project
    )

    return project_detail

def read_project_detail(project_detail_id):
    try:
        project_detail = Project_Detail.objects.get(project_detail_id=project_detail_id)
    except Project_Detail.DoesNotExist:
        return None
    
    return project_detail

def update_project_detail(project_detail_id, image=None, project_id=None):
    try:
        project_detail = Project_Detail.objects.get(project_detail_id=project_detail_id)
    except Project_Detail.DoesNotExist:
        return None

    if image is not None:
        project_detail.image = image
    if project_id is not None:
        project = read_project(project_id)
        if project is not None:
            project_detail.project = project
    
    project_detail.save()
    return project_detail


def delete_project_detail(project_detail_id):
    try:
        project_detail = Project_Detail.objects.get(project_detail_id=project_detail_id)
    except Project_Detail.DoesNotExist:
        return None
    
    project_detail.delete()
    return True