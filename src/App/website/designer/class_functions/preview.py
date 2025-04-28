from ..models import Preview
from .project_detail import read_project_detail

def create_preview(detail_id, final=None):
    detail = read_project_detail(detail_id)
    if detail is None:
        return None
    if final is not None:
        preview = Preview.objects.create(detail=detail, final=True)
    else:
        preview = Preview.objects.create(detail=detail)

    return preview

def read_preview(preview_id):
    try:
        preview = Preview.objects.get(preview_id=preview_id)
    except Preview.DoesNotExist:
        return None
    
    return preview

def update_preview(preview_id, final=None, detail_id=None):
    try:
        preview = Preview.objects.get(preview_id=preview_id)
    except Preview.DoesNotExist:
        return None
    
    if final is not None:
        preview.final = final
    if detail_id is not None:
        detail = read_project_detail(detail_id)
        if detail is None:
            return None
        preview.detail = detail

    preview.save()
    return preview

def delete_preview(preview_id):
    try:
        preview = Preview.objects.get(preview_id=preview_id)
    except Preview.DoesNotExist:
        return None
    
    return preview