from django.contrib import admin
from .models import Patient, Ingreso
from .forms import PatientForm
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    form = PatientForm
    list_display = ('nombre', 'apellido', 'documento')
    list_filter = ('programa', 'genero')
    search_fields = ('nombre', 'apellido', 'documento')
    

class IngresoResource(resources.ModelResource):
    # Esto busca al paciente por su documento en lugar de su ID numérico
    paciente = fields.Field(
        column_name='paciente_id', # Así se debe llamar la columna en tu Excel
        attribute='paciente',
        widget=ForeignKeyWidget(Patient, 'pk') # 'documento' es el campo en tu modelo Patient
    )

    class Meta:
        model = Ingreso
        # Lista aquí todos los campos que vas a subir en el Excel
        fields = ('id', 'paciente', 'fecha_inicio', 'fecha_fin', 'estado', 'motivo')
        import_id_fields = ['id']


@admin.register(Ingreso)
class IngresoAdmin(ImportExportModelAdmin): # <--- Cambiado
    resource_class = IngresoResource # <--- Añadido
    list_display = ('paciente', 'fecha_inicio', 'fecha_fin', 'estado', 'motivo', 'mes_capita')
    list_filter = ('estado',)
    search_fields = ('paciente__nombre', 'paciente__apellido', 'motivo')