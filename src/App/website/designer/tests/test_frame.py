from django.test import TestCase
from ..models import Frame
from ..class_functions.frame import create_frame, read_frame, update_frame, delete_frame

class FrameTests(TestCase):
    def setUp(self):
        self.fake_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f'
        self.name = "frame1"
        self.frame = create_frame(image=self.fake_image_data, name=self.name)

    def test_create_frame(self):
        self.assertIsNotNone(self.frame)
        self.assertEqual(self.name, self.frame.name)
        self.assertEqual(self.fake_image_data, self.frame.image)

    def test_create_frame_none(self):
        frame = create_frame()
        self.assertIsNone(frame)

    def test_read_frame(self):
        read = read_frame(self.frame.frame_id)
        self.assertIsNotNone(read)
        self.assertEqual(read.frame_id, self.frame.frame_id)

    def test_read_frame_dne(self):
        read = read_frame(self.frame.frame_id+1)
        self.assertIsNone(read)

    def test_update_frame(self):
        fake_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x06\x00\x00\x00\xf4\x78\xd4\xfa'
        new_name = "newframe"
        updated = update_frame(frame_id=self.frame.frame_id, image=fake_image_2, name=new_name)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, new_name)
        self.assertEqual(updated.image, fake_image_2)

    def test_update_frame_none(self):
        updated = update_frame(frame_id=self.frame.frame_id)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, self.name)
        self.assertEqual(bytes(updated.image), self.fake_image_data)

    def test_update_frame_dne(self):
        updated = update_frame(frame_id=self.frame.frame_id+1)
        self.assertIsNone(updated)

    def test_delete_frame(self):
        deleted = delete_frame(frame_id=self.frame.frame_id)
        self.assertTrue(deleted)

    def test_detele_frame_dne(self):
        deleted = delete_frame(frame_id=self.frame.frame_id+1)
        self.assertIsNone(deleted)