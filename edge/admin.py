from django.contrib import admin
from .models import Coordinate
from .models import ImPair
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Coordinate)
class CoordinateAdmin(ImportExportModelAdmin):
    list_display = ['__str__', 'created_at']
    ordering=['created_at']

@admin.register(ImPair)
class ImPairAdmin(ImportExportModelAdmin):
    list_display = ['island', '__str__', 'linked']