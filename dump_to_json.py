# dump_to_json.py

import os
import django
from django.core.management import call_command

# Set your Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DocumentManagementSystem.settings")

# Setup Django
django.setup()

# Dump the data
with open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", "--natural-primary", "--natural-foreign", indent=2, stdout=f)
