from ..models import Status
from django.db.utils import IntegrityError

def create_status(name):
    try:
        status = Status.objects.create(name=name)
    except IntegrityError:
        return None
    
    return status

def read_status(status_id):
    try:
        status = Status.objects.get(status_id=status_id)
    except Status.DoesNotExist:
        return None
    
    return status

def update_status(status_id, name):
    try:
        status = Status.objects.get(status_id=status_id)
    except Status.DoesNotExist:
        return None
    
    status.name = name
    try:
        status.save()
    except IntegrityError:
        return None
    
    return status

def delete_status(status_id):
    try:
        status = Status.objects.get(status_id=status_id)
    except Status.DoesNotExist:
        return None
    
    status.delete()
    return True