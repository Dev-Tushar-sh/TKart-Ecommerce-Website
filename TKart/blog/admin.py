from django.contrib import admin

# Register your models here.
from .models import Blogpost #table name

admin.site.register(Blogpost)