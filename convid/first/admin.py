from django.contrib import admin
from .models import Profile,Section



# Register your models here.
class ProfileView(admin.ModelAdmin):
    list_display=[
    'user',
    'dist',
    'phone_no',
    'status',
    ]
class SectionView(admin.ModelAdmin):
        list_display=[
        'user',
        'section_name',
        'status',
        ]


admin.site.register(Profile,ProfileView)
admin.site.register(Section,SectionView)
