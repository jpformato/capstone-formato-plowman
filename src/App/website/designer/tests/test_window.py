from django.test import TestCase
from ..models import Project, User, Project_Detail, Customer, Preview, Window
from ..class_functions.project_detail import create_project_detail
from ..class_functions.project import create_project
from ..class_functions.customer import create_customer
from ..class_functions.preview import create_preview
from ..class_functions.frame import create_frame
from ..class_functions.window import create_window, read_window, update_window, delete_window

class WindowTests(TestCase):
    def setUp(self):
        self.customer = create_customer(first_name="Bruce", last_name="Wayne", email="batman@gmail.com")
        self.employee1 = User.objects.create_user(username='employee1', email='example1@gmail.com', password='1234')
        self.project = create_project(customer_email=self.customer.email, employee_id=self.employee1.id)
        self.fake_image_data_detail = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f' 
        self.project_detail = create_project_detail(self.fake_image_data_detail, self.project.project_id)
        self.preview = create_preview(detail_id=self.project_detail.project_detail_id)
        self.fake_image_data_frame = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        self.frame = create_frame(image=self.fake_image_data_frame, name="frame1")

        self.x1 = 1
        self.x2 = 10
        self.y1 = 2
        self.y2 = 20
        self.window = create_window(preview_id=self.preview.preview_id, x1=self.x1, x2=self.x2, y1=self.y1, y2=self.y2, frame_id=self.frame.frame_id)

    def test_create_window(self):
        self.assertIsNotNone(self.window)
        self.assertEqual(self.preview.preview_id, self.window.preview.preview_id)
        self.assertEqual(self.x1, self.window.x1)
        self.assertEqual(self.frame.frame_id, self.window.frame.frame_id)

    def test_create_window_preview_dne(self):
        window = create_window(preview_id=self.preview.preview_id+1, x1=self.x1, x2=self.x2, y1=self.y1, y2=self.y2, frame_id=self.frame.frame_id)
        self.assertIsNone(window)

    def test_create_window_frame_dne(self):
        window = create_window(preview_id=self.preview.preview_id, x1=self.x1, x2=self.x2, y1=self.y1, y2=self.y2, frame_id=self.frame.frame_id+1)
        self.assertIsNotNone(window)
        self.assertIsNone(window.frame)

    def test_create_window_no_frame(self):
        window = create_window(preview_id=self.preview.preview_id, x1=self.x1, x2=self.x2, y1=self.y1, y2=self.y2)
        self.assertIsNotNone(window)
        self.assertIsNone(window.frame)

    def test_read_window(self):
        read = read_window(self.window.window_id)
        self.assertIsNotNone(read)
        self.assertEqual(self.window.window_id, read.window_id)

    def test_read_window_dne(self):
        read = read_window(self.window.window_id+1)
        self.assertIsNone(read)

    def test_update_window(self):
        new_preview = create_preview(detail_id=self.project_detail.project_detail_id)
        x1 = 2
        x2 = 20
        y1 = 4
        y2 = 40
        new_frame_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        new_frame = create_frame(image=new_frame_image, name="frame2")

        updated = update_window(window_id=self.window.window_id, preview_id=new_preview.preview_id, x1=x1, x2=x2, y1=y1, y2=y2, frame_id=new_frame.frame_id)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.preview.preview_id, new_preview.preview_id)
        self.assertEqual(x1, updated.x1)
        self.assertEqual(updated.frame.frame_id, new_frame.frame_id)

    def test_update_window_dne(self):
        new_preview = create_preview(detail_id=self.project_detail.project_detail_id)
        x1 = 2
        x2 = 20
        y1 = 4
        y2 = 40
        new_frame_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        new_frame = create_frame(image=new_frame_image, name="frame2")

        updated = update_window(window_id=self.window.window_id+1, preview_id=new_preview.preview_id, x1=x1, x2=x2, y1=y1, y2=y2, frame_id=new_frame.frame_id)
        self.assertIsNone(updated)

    def test_update_window_no_change(self):
        updated = update_window(window_id=self.window.window_id)
        self.assertEqual(updated.preview.preview_id, self.window.preview.preview_id)
        self.assertEqual(updated.y2, self.window.y2)
        self.assertEqual(updated.frame.frame_id, self.window.frame.frame_id)

    def delete_window(self):
        deleted = delete_window(window_id=self.window.window_id)
        self.assertTrue(deleted)
    
    def delete_window_dne(self):
        deleted = delete_window(window_id=self.window.window_id+1)
        self.assertIsNone(deleted)