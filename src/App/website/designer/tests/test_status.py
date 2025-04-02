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

    def test_update(self):
        """Test updating a status"""
        new_name = "Accepted"
        updated = update_status(self.status.status_id, new_name)
        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.name, self.status.name)

    def test_delete(self):
        """Test deleting statuses"""
        deleted = delete_status(self.status.status_id)
        self.assertTrue(deleted)