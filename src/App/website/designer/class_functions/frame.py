from ..models import Frame
from django.core.exceptions import ObjectDoesNotExist

def create_frame(image=None, name=None):
    if image is None and name is None:
        return None
    
    frame = Frame.objects.create(image=image, name=name)
    return frame

def read_frame(frame_id):
    try:
        frame = Frame.objects.get(frame_id=frame_id)
    except Frame.DoesNotExist:
        return None
    
    return frame

def update_frame(frame_id, image=None, name=None):
    try:
        frame = Frame.objects.get(frame_id=frame_id)
    except Frame.DoesNotExist:
        return None
    
    if image is not None:
        frame.image = image
    if name is not None:
        frame.name = name
    
    frame.save()
    return frame

def delete_frame(frame_id):
    try:
        frame = Frame.objects.get(frame_id=frame_id)
    except Frame.DoesNotExist:
        return None
    
    frame.delete()
    return True