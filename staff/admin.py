from django.contrib import admin

# Register your models here.
from .models import NewUser,Restaurant,JobPosting,JobApplication
admin.site.register(NewUser)
admin.site.register(Restaurant)
admin.site.register(JobPosting)
admin.site.register(JobApplication)