from django.test import TestCase
from django.contrib.auth import get_user_model
from .class_functions.project import create_project, read_project, update_project, delete_project
from .class_functions.project_detail import create_project_detail, read_project_detail, update_project_detail, delete_project_detail
from .class_functions.window import create_window, read_window, update_window, delete_window

User = get_user_model()

# Create your tests here.

# class PersonTests(TestCase):

#     # Set up person db entry
#     def setUp(self):
#         attributes = {
#             'first_name': "John", 
#             'last_name': "Smith",
#             'email': "example@gmail.com", 
#             'username': "user1", 
#             'password': "password",  
#             'department': "customer"
#         }
#         self.person = create_person(attributes)
    
#     # Make sure it was created
#     def test_create_person(self):
#         self.assertEqual(self.person.email, "example@gmail.com")
#         self.assertEqual(self.person.username, "user1")
    
#     # Test read the person's attributes
#     def test_read_person(self):
#         read = read_person("example@gmail.com")
#         self.assertEqual(read.first_name, self.person.first_name)
    
#     # Test update the person's attributes
#     def test_update_person(self):
#         attributes = {
#             'first_name': "Mathew", 
#             'last_name': "Smith",
#             'email': "example@gmail.com", 
#             'username': "user1", 
#             'password': "password",  
#             'department': "customer"
#         }

#         self.assertEqual(self.person.first_name, "John")
#         update_person(attributes)
#         read = read_person("example@gmail.com")
#         self.assertEqual(read.first_name, "Mathew")

#     # Test deleting the person
#     def test_delete_person(self):
#         delete_person_by_email(self.person.email)
#         read = read_person(self.person.email)
#         self.assertIsNone(read)

# class ProjectTests(TestCase):

#     def setUp(self):
#         personAttr = {
#             'first_name': "John", 
#             'last_name': "Smith",
#             'email': "example@gmail.com", 
#             'username': "user1", 
#             'password': "password",  
#             'department': "customer"
#         }
#         self.person = create_person(personAttr)

#         personAttr1 = {
#             'first_name': "Jane", 
#             'last_name': "Doe",
#             'email': "example1@gmail.com", 
#             'username': "user2", 
#             'password': "1234",  
#             'department': "sales"
#         }
#         self.employee1 = create_person(personAttr1)
#         self.employees = [self.employee1]

#         projectAttr = {
#             "customer_email" : self.person.email,
#         }
#         self.project = create_project(projectAttr)

#     def test_create_project(self):
#         self.assertIsNotNone(self.project)
#         self.assertEqual(self.project.customer, self.person)
    
#     def test_read_project(self):
#         read = read_project(self.project.project_id)
#         self.assertIsNotNone(read)
#         self.assertEqual(self.person, read.customer)

#     def test_update_project(self):
#         attributes = {
#             "project_id" : self.project.project_id,
#             "customer_email" : self.project.customer.email,
#             "employees" : self.employees
#         }

#         updated = update_project(attributes)
#         self.assertIsNotNone(updated)
#         self.assertIn(self.employee1, updated.employees.all())
#         self.assertEqual(len(updated.employees.all()), 1)

#     def test_delete_project(self):
#         deleted = delete_project(self.project.project_id)
#         self.assertTrue(deleted)
#         read = read_project(self.project.project_id)
#         self.assertIsNone(read)

# class ProjectDetailTests(TestCase):
#     def setUp(self):
#         person_attr = {
#             'first_name': "John", 
#             'last_name': "Smith",
#             'email': "example@gmail.com", 
#             'username': "user1", 
#             'password': "password",  
#             'department': "customer"
#         }
#         self.person = create_person(person_attr)

#         person_attr_1 = {
#             'first_name': "Jane", 
#             'last_name': "Doe",
#             'email': "example1@gmail.com", 
#             'username': "user2", 
#             'password': "1234",  
#             'department': "sales"
#         }
#         self.employee1 = create_person(person_attr_1)
#         self.employees = [self.employee1]

#         projectAttr = {
#             "customer_email" : self.person.email,
#         }
#         self.project = create_project(projectAttr)

#         self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        
#         # Create the project detail with binary data
#         attributes = {
#             'image': self.fake_image_data,
#             'project_id': self.project.project_id
#         }
#         self.project_detail = create_project_detail(attributes)

#     def test_create_detail(self):
#         self.assertIsNotNone(self.project_detail)
#         self.assertEqual(self.project_detail.image, self.fake_image_data)

#     def test_read_detail(self):
#         read = read_project_detail(self.project_detail.project_detail_id)
#         self.assertIsNotNone(read)
#         self.assertEqual(self.project_detail.image, bytes(read.image))

#     def test_update_detail(self):
#         fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        
#         project2 = create_project({"customer_email":"example1@gmail.com"})

#         attributes = {
#             'project_detail_id' : self.project_detail.project_detail_id,
#             'image' : fake_image_2,
#             'project_id' : project2
#         }

#         updated = update_project_detail(attributes)
#         self.assertIsNotNone(updated)
#         self.assertEqual(updated.project_id, project2)
#         self.assertEqual(updated.image, fake_image_2)

#     def test_delete_project_detail(self):
#         deleted = delete_project_detail(self.project_detail.project_detail_id)
#         self.assertTrue(deleted)
#         read = read_project_detail(self.project_detail.project_detail_id)
#         self.assertIsNone(read)

# class WindowTestCases(TestCase):
#     def setUp(self):
#         person_attr = {
#             'first_name': "John", 
#             'last_name': "Smith",
#             'email': "example@gmail.com", 
#             'username': "user1", 
#             'password': "password",  
#             'department': "customer"
#         }
#         self.person = create_person(person_attr)

#         person_attr_1 = {
#             'first_name': "Jane", 
#             'last_name': "Doe",
#             'email': "example1@gmail.com", 
#             'username': "user2", 
#             'password': "1234",  
#             'department': "sales"
#         }
#         self.employee1 = create_person(person_attr_1)
#         self.employees = [self.employee1]

#         projectAttr = {
#             "customer_email" : self.person.email,
#         }
#         self.project = create_project(projectAttr)

#         self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        
#         # Create the project detail with binary data
#         attributes = {
#             'image': self.fake_image_data,
#             'project_id': self.project.project_id
#         }
#         self.project_detail = create_project_detail(attributes)

#         window_attr = {
#             'x1' : 30,
#             'y1' : 30,
#             'x2' : 60,
#             'y2' : 60,
#             'project_detail_id' : self.project_detail.project_detail_id
#         }
#         self.window = create_window(window_attr)

#     def test_create_window(self):
#         self.assertIsNotNone(self.window)

class ProjectTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='example@gmail.com', password='password')
        self.employee1 = User.objects.create_user(username='user2', email='example1@gmail.com', password='1234')
        self.employees = [self.employee1]

        project_attr = {"customer_email": self.user.email}
        self.project = create_project(project_attr)

    def test_create_project(self):
        self.assertIsNotNone(self.project)
        self.assertEqual(self.project.customer, self.user)

    def test_create_project_no_customer(self):
        project_attr = {"customer_email": "example3@gmail.com"}
        proj = create_project(project_attr)
        self.assertIsNone(proj)
    
    def test_read_project(self):
        read = read_project(self.project.project_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.user, read.customer)

    def test_read_project_none(self):
        read = read_project(self.project.project_id+1)
        self.assertIsNone(read)

    def test_update_project(self):
        attributes = {
            "project_id": self.project.project_id,
            "customer_email": self.project.customer.email,
            "employees": self.employees
        }

        updated = update_project(attributes)
        self.assertIsNotNone(updated)
        self.assertIn(self.employee1, updated.employees.all())
        self.assertEqual(len(updated.employees.all()), 1)

    def test_update_project_fail(self):
        attributes = {
            "project_id": self.project.project_id+1,
            "customer_email": self.project.customer.email,
            "employees": self.employees
        }

        updated = update_project(attributes)
        self.assertIsNone(updated)

    def test_update_project_no_customer(self):
        attributes = {
            "project_id": self.project.project_id,
            "customer_email": "example3@gmail.com",
            "employees": self.employees
        }

        updated = update_project(attributes)
        self.assertIsNone(updated)

    def test_delete_project(self):
        deleted = delete_project(self.project.project_id)
        self.assertTrue(deleted)

    def test_delete_project_none(self):
        deleted = delete_project(self.project.project_id+1)
        self.assertIsNone(deleted)


class ProjectDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='example@gmail.com', password='password')
        self.employee1 = User.objects.create_user(username='user2', email='example1@gmail.com', password='1234')
        self.employees = [self.employee1]

        project_attr = {"customer_email": self.user.email}
        self.project = create_project(project_attr)

        self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        
        attributes = {
            'image': self.fake_image_data,
            'project_id': self.project.project_id
        }
        self.project_detail = create_project_detail(attributes)

    def test_create_detail(self):
        self.assertIsNotNone(self.project_detail)
        self.assertEqual(self.project_detail.image, self.fake_image_data)

    def test_create_detail_no_project(self):
        attributes = {
            'image': self.fake_image_data,
            'project_id': self.project.project_id+1
        }
        detail = create_project_detail(attributes)

        self.assertIsNone(detail)

    def test_read_detail(self):
        read = read_project_detail(self.project_detail.project_detail_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.project_detail.image, bytes(read.image))

    def test_read_detail_none(self):
        read = read_project_detail(self.project_detail.project_detail_id+1)
        self.assertIsNone(read)

    def test_update_detail(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        
        project2 = create_project({"customer_email": "example1@gmail.com"})

        attributes = {
            'project_detail_id': self.project_detail.project_detail_id,
            'image': fake_image_2,
            'project_id': project2
        }

        updated = update_project_detail(attributes)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.project_id, project2)
        self.assertEqual(updated.image, fake_image_2)

    def test_update_detail_none(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        
        project2 = create_project({"customer_email": "example1@gmail.com"})

        attributes = {
            'project_detail_id': self.project_detail.project_detail_id+1,
            'image': fake_image_2,
            'project_id': project2
        }

        updated = update_project_detail(attributes)
        self.assertIsNone(updated)

    def test_delete_detail(self):
        deleted = delete_project_detail(self.project_detail.project_detail_id)
        self.assertTrue(deleted)

    def test_delete_detail_none(self):
        deleted = delete_project_detail(self.project_detail.project_detail_id+1)
        self.assertIsNone(deleted)


class WindowTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='example@gmail.com', password='password')
        self.employee1 = User.objects.create_user(username='user2', email='example1@gmail.com', password='1234')
        self.employees = [self.employee1]

        project_attr = {"customer_email": self.user.email}
        self.project = create_project(project_attr)

        self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        
        attributes = {
            'image': self.fake_image_data,
            'project_id': self.project.project_id
        }
        self.project_detail = create_project_detail(attributes)

        window_attr = {
            'x1': 30,
            'y1': 30,
            'x2': 60,
            'y2': 60,
            'project_detail_id': self.project_detail.project_detail_id
        }
        self.window = create_window(window_attr)

    def test_create_window(self):
        self.assertIsNotNone(self.window)

    def test_create_window_no_detail(self):
        window_attr = {
            'x1': 30,
            'y1': 30,
            'x2': 60,
            'y2': 60,
            'project_detail_id': self.project_detail.project_detail_id+1
        }
        window = create_window(window_attr)
        self.assertIsNone(window)

    def test_read_window(self):
        read = read_window(self.window.window_id)
        self.assertIsNotNone(read)
        self.assertEqual(read.project_detail_id, self.project_detail)

    def test_read_window_none(self):
        read = read_window(self.window.window_id+1)
        self.assertIsNone(read)

    def test_update_window(self):
        new_attr = {
            'window_id' : self.window.window_id,
            'x1' : 100,
            'y1' : 110,
            'x2' : 120,
            'y2' : 130
        }

        updated = update_window(new_attr)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.x1, 100)
        self.assertEqual(updated.y2, 130)

    def test_update_window_none(self):
        new_attr = {
            'window_id' : self.window.window_id+1,
            'x1' : 100,
            'y1' : 110,
            'x2' : 120,
            'y2' : 130
        }

        updated = update_window(new_attr)
        self.assertIsNone(updated)

    def test_delete_window(self):
        deleted = delete_window(self.window.window_id)
        self.assertTrue(deleted)

    def test_delete_window_none(self):
        deleted = delete_window(self.window.window_id+1)
        self.assertIsNone(deleted)