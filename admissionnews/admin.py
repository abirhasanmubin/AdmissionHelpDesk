from django.contrib import admin
from .models import University, AdmissionNews, Comment
# Register your models here.

admin.site.register(University)
admin.site.register(AdmissionNews)
admin.site.register(Comment)
