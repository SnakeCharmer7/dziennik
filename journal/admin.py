from django.contrib import admin

from . import models


admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.StudentClass)
admin.site.register(models.School)
admin.site.register(models.Grade)
admin.site.register(models.Subject)