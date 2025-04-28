from django.test import TestCase
from ..models import Status
from ..class_functions.status import create_status, read_status, update_status, delete_status

class StatusTests(TestCase):
    def setUp(self):
        name = "Created"
        self.status = create_status(name)

    def test_create(self):
        """Test creating a status"""
        self.assertIsNotNone(self.status)
        self.assertEqual(self.status.name, "Created")

    def test_read(self):
        """Test reading a status from the db"""
        read = read_status(self.status.status_id)
        self.assertIsNotNone(read)
        self.assertEqual(read.name, self.status.name)

    def test_read_dne(self):
        """Test reading a status from the db when it doesn't exist"""
        read = read_status(self.status.status_id+1)
        self.assertIsNone(read)

    def test_update(self):
        """Test updating a status"""
        new_name = "Accepted"
        updated = update_status(self.status.status_id, new_name)
        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.name, self.status.name)

    def test_update_dne(self):
        """Test updating a status when it doesn't"""
        new_name = "Accepted"
        updated = update_status(self.status.status_id+1, new_name)
        self.assertIsNone(updated)

    def test_delete(self):
        """Test deleting statuses"""
        deleted = delete_status(self.status.status_id)
        self.assertTrue(deleted)

    def test_delete(self):
        """Test deleting statuses when it doesn't exist"""
        deleted = delete_status(self.status.status_id+1)
        self.assertIsNone(deleted)