from django.contrib import admin
from .models import Patient, Ingreso
from .forms import PatientForm

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm
    list_display = ('nombre', 'apellido', 'documento')
    list_filter = ('programa', 'genero')
    search_fields = ('nombre', 'apellido', 'documento')
    

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_inicio', 'fecha_fin', 'estado', 'motivo', 'mes_capita')
    list_filter = ('estado',)
    search_fields = ('paciente__nombre', 'paciente__apellido', 'motivo')
    