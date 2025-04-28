from ..models import Window, Preview, Frame
from .preview import read_preview
from .frame import read_frame
from django.core.exceptions import ObjectDoesNotExist

def create_window(preview_id, x1, y1, x2, y2, frame_id=None):
    preview = read_preview(preview_id)
    if preview is None:
        return None
    
    if frame_id is not None:
        frame = read_frame(frame_id=frame_id)
        if frame is None:
            frame = None
    else:
        frame = None

    window = Window.objects.create(
        x1 = x1,
        y1 = y1,
        x2 = x2,
        y2 = y2,
        preview = preview,
        frame = frame
    )

    return window

def read_window(window_id):
    try:
        window = Window.objects.get(window_id=window_id)
    except Window.DoesNotExist:
        return None
    
    return window

def update_window(window_id, preview_id=None, x1=None, y1=None, x2=None, y2=None, frame_id=None):
    try:
        window = Window.objects.get(window_id=window_id)
    except Window.DoesNotExist:
        return None
    
    if preview_id is not None:
        new_preview = read_preview(preview_id=preview_id)
        if new_preview is not None:
            window.preview = new_preview
    if x1 is not None:
        window.x1 = x1
    if y1 is not None:
        window.y1 = y1
    if x2 is not None:
        window.x2 = x2
    if y2 is not None:
        window.y2 = y2
    if frame_id is not None:
        new_frame = read_frame(frame_id=frame_id)
        if new_frame is not None:
            window.frame = new_frame

    window.save()
    return window

def delete_window(window_id):
    try:
        window = Window.objects.get(window_id=window_id)
    except Window.DoesNotExist:
        return None
    
    window.delete()
    return True