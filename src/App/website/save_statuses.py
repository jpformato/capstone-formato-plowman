import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")  # Use website.settings here
django.setup()

from designer.models import Status

Status.objects.get_or_create(name="Contract")
Status.objects.get_or_create(name="Final Measure")
Status.objects.get_or_create(name="Order")
Status.objects.get_or_create(name="ETA")
Status.objects.get_or_create(name="Installation")