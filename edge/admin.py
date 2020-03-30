from django.contrib import admin
from .models import Coordinate
from .models import ImPair
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Coordinate)
class CoordinateAdmin(ImportExportModelAdmin):
    pass
admin.site.register(ImPair)

