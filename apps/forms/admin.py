from django.contrib import admin
from models import Job, Pravila, UserProfile, JobType, Towns_and_regoins



admin.site.register(Job)
admin.site.register(Towns_and_regoins)
admin.site.register(JobType)
admin.site.register(Pravila)
admin.site.register(UserProfile)

