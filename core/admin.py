from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Student


# admin.site.register(User)
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    pass
