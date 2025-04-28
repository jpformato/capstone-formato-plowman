import os
import django
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")  # Use website.settings here
django.setup()

from designer.models import Frame

def load_frames_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            with open(os.path.join(folder_path, filename), "rb") as f:
                image_data = f.read()
                Frame.objects.create(
                    name=os.path.splitext(filename)[0],
                    image=image_data
                )
                print(f"Saved: {filename}")

load_frames_from_folder("C:/Users/jackf/Documents/School Work/Capstone/capstone-formato-plowman/src/App/website/designer/frame_images")
