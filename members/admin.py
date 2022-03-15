from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

admin.site.register(Modulos)
