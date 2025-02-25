from django.test import TestCase
from .models import Person
from .class_functions.person import create_person, read_person, update_person, delete_person_by_email, delete_person_by_id, check_new_password
from .class_functions.project import create_project, read_project, update_project, delete_project
from .class_functions.project_detail import create_project_detail, read_project_detail, update_project_detail, delete_project_detail


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
        self.assertEqual(read.first_name, self.person.first_name)
    
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
        self.assertEqual(read.first_name, "Mathew")

    # Test deleting the person
    def test_delete_person(self):
        delete_person_by_email(self.person.email)
        read = read_person(self.person.email)
        self.assertIsNone(read)

class ProjectTests(TestCase):

    def setUp(self):
        personAttr = {
            'first_name': "John", 
            'last_name': "Smith",
            'email': "example@gmail.com", 
            'username': "user1", 
            'password': "password",  
            'department': "customer"
        }
        self.person = create_person(personAttr)

        personAttr1 = {
            'first_name': "Jane", 
            'last_name': "Doe",
            'email': "example1@gmail.com", 
            'username': "user2", 
            'password': "1234",  
            'department': "sales"
        }
        self.employee1 = create_person(personAttr1)
        self.employees = [self.employee1]

        projectAttr = {
            "customer_email" : self.person.email,
        }
        self.project = create_project(projectAttr)

    def test_create_project(self):
        self.assertIsNotNone(self.project)
        self.assertEqual(self.project.customer, self.person)
    
    def test_read_project(self):
        read = read_project(self.project.project_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.person, read.customer)

    def test_update_project(self):
        attributes = {
            "project_id" : self.project.project_id,
            "customer_email" : self.project.customer.email,
            "employees" : self.employees
        }

        updated = update_project(attributes)
        self.assertIsNotNone(updated)
        self.assertIn(self.employee1, updated.employees.all())
        self.assertEqual(len(updated.employees.all()), 1)

    def test_delete_project(self):
        deleted = delete_project(self.project.project_id)
        self.assertTrue(deleted)
        read = read_project(self.project.project_id)
        self.assertIsNone(read)

class ProjectDetailTests(TestCase):
    def setUp(self):
        person_attr = {
            'first_name': "John", 
            'last_name': "Smith",
            'email': "example@gmail.com", 
            'username': "user1", 
            'password': "password",  
            'department': "customer"
        }
        self.person = create_person(person_attr)

        person_attr_1 = {
            'first_name': "Jane", 
            'last_name': "Doe",
            'email': "example1@gmail.com", 
            'username': "user2", 
            'password': "1234",  
            'department': "sales"
        }
        self.employee1 = create_person(person_attr_1)
        self.employees = [self.employee1]

        projectAttr = {
            "customer_email" : self.person.email,
        }
        self.project = create_project(projectAttr)

        self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        
        # Create the project detail with binary data
        attributes = {
            'image': self.fake_image_data,
            'project_id': self.project.project_id
        }
        self.project_detail = create_project_detail(attributes)

    def test_create_detail(self):
        self.assertIsNotNone(self.project_detail)
        self.assertEqual(self.project_detail.image, self.fake_image_data)

    def test_read_detail(self):
        read = read_project_detail(self.project_detail.project_detail_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.project_detail.image, bytes(read.image))

    def test_update_detail(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        
        project2 = create_project({"customer_email":"example1@gmail.com"})

        attributes = {
            'project_detail_id' : self.project_detail.project_detail_id,
            'image' : fake_image_2,
            'project_id' : project2
        }

        updated = update_project_detail(attributes)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.project_id, project2)
        self.assertEqual(updated.image, fake_image_2)

    def test_delete_project_detail(self):
        deleted = delete_project_detail(self.project_detail.project_detail_id)
        self.assertTrue(deleted)
        read = read_project_detail(self.project_detail.project_detail_id)
        self.assertIsNone(read)