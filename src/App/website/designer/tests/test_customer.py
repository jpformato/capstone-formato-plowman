from django.test import TestCase
from ..models import Customer
from ..class_functions.customer import create_customer, read_customer, read_customer_email, update_customer, delete_customer

class CustomerTests(TestCase):
    def setUp(self):
        self.first_name = "Bruce"
        self.last_name = "Wayne"
        self.email = "batman@gmail.com"
        self.customer = create_customer(first_name=self.first_name, last_name=self.last_name, email=self.email)

    def test_create(self):
        """Test to see if the customer was created properly"""
        self.assertIsNotNone(self.customer)
        self.assertEqual(self.customer.email, self.email)

    def test_create_no_name(self):
        email2 = "wayne@gmail.com"
        customer2 = create_customer(email=email2)
        self.assertIsNotNone(customer2)
        self.assertEqual(customer2.email, email2)
    
    def test_read_id(self):
        """Test if we can read a customer by their id"""
        read = read_customer(self.customer.customer_id)
        self.assertIsNotNone(read)
        self.assertEqual(read.email, self.customer.email)
    
    def test_read_id_dne(self):
        """Test if we get none for reading a customer that doesn't exist"""
        read = read_customer(self.customer.customer_id+1)
        self.assertIsNone(read)

    def test_read_email(self):
        """Test if we can read a customer by their email"""
        read = read_customer_email(self.customer.email)
        self.assertIsNotNone(read)
        self.assertEqual(read, self.customer)

    def test_read_email_dne(self):
        """Test if we get none for reading a customer that doesn't exist by email"""
        read = read_customer_email("wayne@gmail.com")
        self.assertIsNone(read)

    def test_update_dne(self):
        """Test if update works when we customer doesn't exist"""
        first_name = "Damian"
        updated = update_customer(self.customer.customer_id+1, first_name=first_name)
        self.assertIsNone(updated)

    def test_update_first_name(self):
        """Test if first name updates properly"""
        first_name = "Damian"
        updated = update_customer(self.customer.customer_id, first_name=first_name)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.first_name, first_name)

    def test_update_last_name(self):
        """Test if last name updates properly"""
        last_name = "Kent"
        updated = update_customer(self.customer.customer_id, last_name=last_name)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.last_name, last_name)
    
    def test_update_email(self):
        """Test if email updates properly"""
        email = "wayne@gmail.com"
        updated = update_customer(self.customer.customer_id, email=email)
        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.email, self.customer.email)

    def test_delete(self):
        """Test if customer is deleted"""
        deleted = delete_customer(self.customer.customer_id)
        self.assertTrue(deleted)