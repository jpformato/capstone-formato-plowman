from django.test import TestCase
from ..models import Project, User, Project_Detail, Customer
from ..class_functions.project_detail import create_project_detail, read_project_detail, update_project_detail, delete_project_detail
from ..class_functions.project import create_project
from ..class_functions.customer import create_customer


class ProjectDetailTests(TestCase):
    def setUp(self):
        self.customer = create_customer(first_name="Bruce", last_name="Wayne", email="batman@gmail.com")
        self.employee1 = User.objects.create_user(username='employee1', email='example1@gmail.com', password='1234')
        self.project = create_project(customer_email=self.customer.email, employee_id=self.employee1.id)

        self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        self.project_detail = create_project_detail(self.fake_image_data, self.project.project_id)

    def test_create_detail(self):
        self.assertIsNotNone(self.project_detail)
        self.assertEqual(self.project_detail.image, self.fake_image_data)
        self.assertEqual(self.project.project_id, self.project_detail.project.project_id)

    def test_create_detail_no_project(self):
        detail = create_project_detail(self.fake_image_data, self.project.project_id+1)
        self.assertIsNone(detail)

    def test_read_detail(self):
        read = read_project_detail(self.project_detail.project_detail_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.project_detail.image, bytes(read.image))

    def test_read_detail_none(self):
        read = read_project_detail(self.project_detail.project_detail_id+1)
        self.assertIsNone(read)

    def test_update_detail_image(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        updated = update_project_detail(self.project_detail.project_detail_id, image=fake_image_2)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.image, fake_image_2)

    def test_update_detail_project(self):
        employee2 = User.objects.create_user(username='employee2', email='example1@gmail.com', password='1234')
        project2 = create_project(self.customer, employee2.id)
        updated = update_project_detail(self.project_detail.project_detail_id, project_id=project2.project_id)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.project.project_id, project2.project_id)

    def test_update_detail_none(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        updated = update_project_detail(project_detail_id=self.project_detail.project_detail_id+1, image=fake_image_2)
        self.assertIsNone(updated)

    def test_delete_detail(self):
        deleted = delete_project_detail(self.project_detail.project_detail_id)
        self.assertTrue(deleted)

    def test_delete_detail_none(self):
        deleted = delete_project_detail(self.project_detail.project_detail_id+1)
        self.assertIsNone(deleted)