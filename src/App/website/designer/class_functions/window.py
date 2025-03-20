from ..models import Window, Project_Detail
from .project_detail import read_project_detail

def create_window(attributes):
    project_detail = read_project_detail(attributes['project_detail_id'])
    if project_detail is None:
        return None
    x1 = attributes['x1']
    y1 = attributes['y1']
    x2 = attributes['x2']
    y2 = attributes['y2']

    window = Window.objects.create(
        x1 = x1,
        y1 = y1,
        x2 = x2,
        y2 = y2,
        project_detail_id = project_detail
    )

    return window

def read_window(window_id):
    try:
        window = Window.objects.get(window_id=window_id)
    except Window.DoesNotExist:
        return None
    
    return window

def update_window(attributes):
    try:
        window = Window.objects.get(window_id=attributes['window_id'])
    except Window.DoesNotExist:
        return None
    
    window.x1 = attributes['x1']
    window.y1 = attributes['y1']
    window.x2 = attributes['x2']
    window.y2 = attributes['y2']
    window.save()

    return window

def delete_window(window_id):
    try:
        window = Window.objects.get(window_id=window_id)
    except Window.DoesNotExist:
        return None
    
    window.delete()
    return True