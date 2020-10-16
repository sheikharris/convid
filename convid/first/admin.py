from django.contrib import admin
from .models import Profile



# Register your models here.
class ProfileView(admin.ModelAdmin):
    list_display=[
    'user',
    'dist',
    'phone_no',
    'status',
    ]

admin.site.register(Profile,ProfileView)
