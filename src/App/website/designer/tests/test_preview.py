from django.test import TestCase
from ..models import Project, User, Project_Detail, Customer, Preview
from ..class_functions.project_detail import create_project_detail
from ..class_functions.project import create_project
from ..class_functions.customer import create_customer
from ..class_functions.preview import create_preview, read_preview, update_preview, delete_preview

class PreviewTests(TestCase):
    def setUp(self):
        self.customer = create_customer(first_name="Bruce", last_name="Wayne", email="batman@gmail.com")
        self.employee1 = User.objects.create_user(username='employee1', email='example1@gmail.com', password='1234')
        self.project = create_project(customer_email=self.customer.email, employee_id=self.employee1.id)
        self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        self.project_detail = create_project_detail(self.fake_image_data, self.project.project_id)

        self.preview = create_preview(detail_id=self.project_detail.project_detail_id)

    def test_create_preview(self):
        self.assertIsNotNone(self.preview)
        self.assertEqual(self.preview.detail.project_detail_id, self.project_detail.project_detail_id)
        self.assertEqual(self.preview.final, False)

    def test_create_preview_final(self):
        preview = create_preview(detail_id=self.project_detail.project_detail_id, final=True)
        self.assertIsNotNone(preview)
        self.assertEqual(preview.detail.project_detail_id, self.project_detail.project_detail_id)
        self.assertEqual(preview.final, True)

    def test_create_preview_detail_dne(self):
        preview = create_preview(detail_id=self.project_detail.project_detail_id+1)
        self.assertIsNone(preview)

    def test_read_preview(self):
        read = read_preview(self.preview.preview_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.preview.detail.project_detail_id, read.detail.project_detail_id)

    def test_read_preview_dne(self):
        read = read_preview(self.preview.preview_id+1)
        self.assertIsNone(read)
    
    def test_update_preview(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        detail = create_project_detail(fake_image_2, self.project.project_id)
        updated = update_preview(preview_id=self.preview.preview_id, final=True, detail_id=detail.project_detail_id)

        self.assertIsNotNone(updated)
        self.assertNotEqual(updated.detail.project_detail_id, self.preview.detail.project_detail_id)
        self.assertEqual(updated.detail.project_detail_id, detail.project_detail_id)
        self.assertEqual(updated.final, True)

    def test_update_preview_dne(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        detail = create_project_detail(fake_image_2, self.project.project_id)
        updated = update_preview(preview_id=self.preview.preview_id+1, final=True, detail_id=detail.project_detail_id)
        self.assertIsNone(updated)

    def test_update_preview_detail_dne(self):
        updated = update_preview(preview_id=self.preview.preview_id+1, final=True, detail_id=self.project_detail.project_detail_id+1)
        self.assertIsNone(updated)

    def test_update_preview_no_update(self):
        updated = update_preview(preview_id=self.preview.preview_id)
        self.assertIsNotNone(updated)

    def test_delete_preview(self):
        deleted = delete_preview(self.preview.preview_id)
        self.assertTrue(deleted)

    def test_delete_preview_dne(self):
        deleted = delete_preview(self.preview.preview_id+1)
        self.assertIsNone(deleted)