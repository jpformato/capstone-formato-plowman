from django.test import TestCase
from ..models import Project, User, Customer, Status
from ..class_functions.project import create_project, read_project, update_project, delete_project, read_project_tracking, add_employee, start_project, next
from ..class_functions.customer import create_customer
from ..class_functions.status import create_status


class ProjectTests(TestCase):
    def setUp(self):
        self.customer = create_customer("Bruce", "Wayne", "batman@gmail.com")
        self.employee1 = User.objects.create_user(username='employee1', email='example@gmail.com', password='1234')
        self.project = create_project(self.customer.email, self.employee1.id)

    def test_create_project(self):
        self.assertIsNotNone(self.project)
        self.assertEqual(self.project.customer, self.customer)
        self.assertEqual(self.project.employees.count(), 1)

    def test_create_project_no_customer(self):
        proj = create_project("superman@gamil.com", self.employee1.id)
        self.assertIsNone(proj)
    
    def test_read_project(self):
        read = read_project(self.project.project_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.customer.email, read.customer.email)

    def test_read_project_none(self):
        read = read_project(self.project.project_id+1)
        self.assertIsNone(read)

    def test_update_project(self):
        customer2 = create_customer("Clark", "Kent", "superman@gmail.com")
        updated = update_project(self.project.project_id, customer_email=customer2.email)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.customer.email, customer2.email)

    def test_update_project_fail(self):
        customer2 = create_customer("Clark", "Kent", "superman@gmail.com")
        updated = update_project(self.project.project_id+1, customer_email=customer2.email)
        self.assertIsNone(updated)

    def test_update_project_no_customer(self):
        updated = update_project(self.project.project_id+1, customer_email="superman@gmail.com")
        self.assertIsNone(updated)

    def test_delete_project(self):
        deleted = delete_project(self.project.project_id)
        self.assertTrue(deleted)

    def test_delete_project_none(self):
        deleted = delete_project(self.project.project_id+1)
        self.assertIsNone(deleted)

    def test_start(self):
        status = create_status("Created")
        started = start_project(self.project.project_id)
        self.assertIsNotNone(started)
        self.assertEqual(started.statuses.count(), 1)

        new_stat = started.statuses.first()
        self.assertIsNotNone(new_stat)
        self.assertEqual(new_stat.name, status.name)

        # TESTS:
        # - next with no status
        # - next with a status
        # - next when complete
        # - *maybe* gen tracking number