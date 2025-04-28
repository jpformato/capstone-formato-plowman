from ..models import Customer
from django.db.utils import IntegrityError

def create_customer(email, first_name=None, last_name=None):
    try:
        if first_name is None or last_name is None:
            customer = Customer.objects.create(
                email = email
            )
        else:
            customer = Customer.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email
            )
    except IntegrityError:
        return None

    return customer

def read_customer(customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None
    
    return customer

def read_customer_email(customer_email):
    try:
        customer = Customer.objects.get(email=customer_email)
    except Customer.DoesNotExist:
        return None
    
    return customer

def update_customer(customer_id, first_name=None, last_name=None, email=None):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None
    
    
    if first_name is not None:
        customer.first_name = first_name
    if last_name is not None:
        customer.last_name = last_name
    if email is not None:
        try:
            customer.email = email
        except IntegrityError:
            return None
    
    customer.save()
    return customer

def delete_customer(customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None
    
    customer.delete()
    return True