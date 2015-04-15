from django.contrib import admin
from models import Job, Pravila, UserProfile, JobType



admin.site.register(Job)
admin.site.register(JobType)
admin.site.register(Pravila)
admin.site.register(UserProfile)

