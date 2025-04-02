from ..models import Preview
from .project_detail import read_project_detail

def create_preview(detail_id):
    detail = read_project_detail(detail_id)
    if detail is None:
        return None
    
    preview = Preview.objects.create(detail=detail)

    return preview

def read_preview(preview_id):
    try:
        preview = Preview.objects.get(preview_id=preview_id)
    except Preview.DoesNotExist:
        return None
    
    return preview

# SHOULD NEVER UPDATE A PREVIEW

def delete_preview(preview_id):
    try:
        preview = Preview.objects.get(preview_id=preview_id)
    except Preview.DoesNotExist:
        return None
    
    return preview