from django.test import TestCase
from ..models import Project, User, Customer, Status
from ..class_functions.project import create_project, read_project, update_project, delete_project, read_project_order, add_employee, start_project
from ..class_functions.customer import create_customer
from ..class_functions.status import create_status


class ProjectTests(TestCase):
    def setUp(self):
        self.customer = create_customer(first_name="Bruce", last_name="Wayne", email="batman@gmail.com")
        self.employee1 = User.objects.create_user(username='employee1', email='example@gmail.com', password='1234')
        self.project = create_project(self.customer.email, self.employee1.id)

    def test_create_project(self):
        self.assertIsNotNone(self.project)
        self.assertEqual(self.project.customer, self.customer)
        self.assertEqual(self.project.employees.count(), 1)

    def test_create_project_no_customer(self):
        proj = create_project("superman@gamil.com", self.employee1.id)
        self.assertIsNotNone(proj)
        self.assertEqual(proj.customer.email, "superman@gamil.com")

    def test_create_project_no_employee(self):
        proj = create_project("superman@gamil.com", self.employee1.id+1)
        self.assertIsNone(proj)
    
    def test_read_project(self):
        read = read_project(self.project.project_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.customer.email, read.customer.email)

    def test_read_project_none(self):
        read = read_project(self.project.project_id+1)
        self.assertIsNone(read)

    def test_read_project_order(self):
        read = read_project_order(self.project.order_number)
        self.assertIsNotNone(read)
        self.assertEqual(read.project_id, self.project.project_id)

    def test_read_project_order_dne(self):
        read = read_project_order("12345678")
        self.assertIsNone(read)

    def test_update_project(self):
        customer2 = create_customer("Clark", "Kent", "superman@gmail.com")
        updated = update_project(self.project.project_id, customer_email=customer2.email)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.customer.email, customer2.email)

    def test_update_project_customer_dne(self):
        updated = update_project(self.project.project_id, customer_email="superman@gmail.com")
        self.assertIsNone(updated)

    def test_update_project_fail(self):
        customer2 = create_customer("Clark", "Kent", "superman@gmail.com")
        updated = update_project(self.project.project_id+1, customer_email=customer2.email)
        self.assertIsNone(updated)

    def test_update_project_no_project(self):
        updated = update_project(self.project.project_id+1, customer_email="superman@gmail.com")
        self.assertIsNone(updated)

    def test_update_project_employees(self):
        employee2 = User.objects.create_user(username='employee2', email='example2@gmail.com', password='1234')
        employee3 = User.objects.create_user(username='employee3', email='example3@gmail.com', password='1234')
        employees = [employee2.email, employee3.email]
        updated = update_project(self.project.project_id, employees=employees)
        self.assertIsNotNone(updated)
        self.assertEqual(3, self.project.employees.count())
    
    def test_add_employee(self):
        employee2 = User.objects.create_user(username='employee2', email='example2@gmail.com', password='1234')
        updated = add_employee(project_id=self.project.project_id, employee_email=employee2.email)
        self.assertIsNotNone(updated)
        self.assertEqual(2, updated.employees.count())

    def test_add_employee_employee_dne(self):
        updated = add_employee(project_id=self.project.project_id, employee_email='example2@gmail.com')
        self.assertIsNone(updated)

    def test_add_employee_project_dne(self):
        employee2 = User.objects.create_user(username='employee2', email='example2@gmail.com', password='1234')
        updated = add_employee(project_id=self.project.project_id+1, employee_email=employee2.email)
        self.assertIsNone(updated)

    def test_delete_project(self):
        deleted = delete_project(self.project.project_id)
        self.assertTrue(deleted)

    def test_delete_project_none(self):
        deleted = delete_project(self.project.project_id+1)
        self.assertIsNone(deleted)

    def test_start(self):
        status1 = create_status("Contract")
        status2 = create_status("Final Measure")
        status3 = create_status("Order")
        status4 = create_status("ETA")
        status5 = create_status("Installation")
        started = start_project(self.project.project_id)
        self.assertIsNotNone(started)
        self.assertEqual(started.statuses.count(), 5)

        new_stat = started.statuses.first()
        self.assertIsNotNone(new_stat)
        self.assertEqual(new_stat.name, status1.name)