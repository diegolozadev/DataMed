from django.contrib import admin
from .models import Patient

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'tipo_documento', 'documento', 'fecha_nacimiento', 'ciudad', 'departamento', 'fecha_ingreso')
    search_fields = ('nombre', 'apellido', 'documento')
    list_filter = ('departamento', 'ciudad', 'tipo_documento')