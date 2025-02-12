from ..models import Person

def create_person(attributes):
    """Create a new person in the db"""
    first_name = attributes['first_name']
    last_name = attributes['last_name']
    email = attributes['email']
    username = attributes['username']
    password = attributes['password']
    department = attributes['department']

    person = Person.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        username = username,
        password = password,
        department = department
    )

    return person

def read_person(email):
    """Read a person's attributes from the db"""
    person = Person.objects.filter(email=email).first()

    if not person:
        return False
    
    attributes = {
        'first_name': person.first_name, 
        'last_name': person.last_name,
        'email': person.email, 
        'username': person.username, 
        'password': person.password,  
        'department': person.department
    }

    return attributes

def update_person(attributes):
    """Update a person's attributes in the db"""
    first_name = attributes['first_name']
    last_name = attributes['last_name']
    email = attributes['email']
    username = attributes['username']
    password = attributes['password']
    department = attributes['department']

    person = Person.objects.filter(email=email).first()

    if not person:
        return False
        
    person.first_name = first_name
    person.last_name = last_name
    person.email = email
    person.username = username
    person.password = password
    person.department = department
    person.save()

    return True

def delete_person_by_id(person_id):
    """Delete a person in the database by their id"""
    person = Person.objects.filter(person_id=person_id).first()
    
    if person:
        person.delete()
        return True
    else:
        return False
    
def delete_person_by_email(email):
    """Delete a person in the database by their email"""
    person = Person.objects.filter(email=email).first()
    
    if not person:
        return False
    
    person.delete()
    return True
    
def check_new_password(email):
    """Check if a person has a password"""
    person = Person.objects.filter(email=email).first()

    if not person:
        return False
    
    if person.password:
        return False
    
    return True
    
