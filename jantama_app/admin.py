from django.contrib import admin

# Register your models here.
from .models import User, Match

admin.site.register(User)
admin.site.register(Match)