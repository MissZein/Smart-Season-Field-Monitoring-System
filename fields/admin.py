from django.contrib import admin
from .models import Field # Import your model

# This line tells Django to show "Fields" in the admin panel
admin.site.register(Field)