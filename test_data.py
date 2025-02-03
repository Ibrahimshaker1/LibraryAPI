import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_api.settings')

import django
django.setup()

from library import models


if __name__ == "__main__":
    pass