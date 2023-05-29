from django.contrib import admin
from .models import custom_user

# Register your models here.
admin.site.register(custom_user)


def __str__(self):
    return f"Username: {self.username}, First Name: {self.first_name}, Email: {self.email}"


