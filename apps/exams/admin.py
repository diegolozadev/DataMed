from django.contrib import admin
from .models import Monitoreo, Psicologia, Nutricion

# Register your models here.

# Registro del modelo Monitoreo en el admin de Django
@admin.register(Monitoreo)
class MonitoreoAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'modo_ventilatorio',
        'uso_diario',
        'hipopnea_residual',
        'etco2_promedio',
        'registrado_por',
        'created_at',
    )

    list_filter = (
        'modo_ventilatorio',
        'mascara_cpap',
        'tamano_mascara',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# Registro del modelo Psicologia en el admin de Django
@admin.register(Psicologia)
class PsicologiaAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'inventario_depre_beck',
        'inventario_ansiedad_beck',
        'escala_atenas',
        'registrado_por',
        'created_at',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# Registro del modelo Nutricion en el admin de Django
@admin.register(Nutricion)
class NutricionAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'estado_nutricional',
        'carbohidratos_pct',
        'rumiacion',
        'registrado_por',
        'created_at',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'