from django.test import TestCase
from ..models import Customer
from ..class_functions.customer import create_customer, read_customer, read_customer_email, update_customer, delete_customer

class CustomerTests(TestCase):
    def setUp(self):
        self.first_name = "Bruce"
        self.last_name = "Wayne"
        self.email = "batman@gmail.com"
        self.customer = create_customer(self.first_name, self.last_name, self.email)

    def test_create(self):
        """Test to see if the customer was created properly"""
        self.assertIsNotNone(self.customer)
        self.assertEqual(self.customer.email, self.email)
    
    def test_read_id(self):
        """Test if we can read a customer by their id"""
        read = read_customer(self.customer.customer_id)
        self.assertIsNotNone(read)
        self.assertEqual(read.email, self.customer.email)

    def test_read_email(self):
        """Test if we can read a customer by their email"""
        read = read_customer_email(self.customer.email)
        self.assertIsNotNone(read)
        self.assertEqual(read, self.customer)

    def test_update_first_name(self):
        """Test if first name updates properly"""
        first_name = "Damian"
        updated = update_customer(self.customer.customer_id, first_name=first_name)
        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.first_name, self.customer.first_name)

    def test_update_last_name(self):
        """Test if last name updates properly"""
        last_name = "Kent"
        updated = update_customer(self.customer.customer_id, last_name=last_name)
        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.last_name, self.customer.last_name)
    
    def test_update_last_name(self):
        """Test if email updates properly"""
        email = "wayne@gmail.com"
        updated = update_customer(self.customer.customer_id, email=email)
        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.email, self.customer.email)

    def test_delete(self):
        """Test if customer is deleted"""
        deleted = delete_customer(self.customer.customer_id)
        self.assertTrue(deleted)