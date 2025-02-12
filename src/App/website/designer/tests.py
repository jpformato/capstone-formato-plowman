from django.test import TestCase
from .models import Person
from .class_functions.person import create_person, read_person, update_person, delete_person_by_email, delete_person_by_id, check_new_password


# Create your tests here.

class PersonTests(TestCase):

    # Set up person db entry
    def setUp(self):
        attributes = {
        'first_name': "John", 
        'last_name': "Smith",
        'email': "example@gmail.com", 
        'username': "user1", 
        'password': "password",  
        'department': "customer"
        }
        self.person = create_person(attributes)
    
    # Make sure it was created
    def test_create_person(self):
        self.assertEqual(self.person.email, "example@gmail.com")
        self.assertEqual(self.person.username, "user1")
    
    # Test read the person's attributes
    def test_read_person(self):
        read = read_person("example@gmail.com")
        self.assertEqual(read['first_name'], self.person.first_name)
    
    # Test update the person's attributes
    def test_update_person(self):
        attributes = {
            'first_name': "Mathew", 
            'last_name': "Smith",
            'email': "example@gmail.com", 
            'username': "user1", 
            'password': "password",  
            'department': "customer"
        }

        self.assertEqual(self.person.first_name, "John")
        update_person(attributes)
        read = read_person("example@gmail.com")
        self.assertEqual(read['first_name'], "Mathew")

    # Test deleting the person
    def test_delete_person(self):
        delete_person_by_email(self.person.email)
        self.assertFalse(read_person(self.person.email))