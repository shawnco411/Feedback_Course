from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.course)
admin.site.register(models.Homework)
admin.site.register(models.SubmitWork)
admin.site.register(models.Resource)
