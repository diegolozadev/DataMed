from django.contrib import admin
from .models import Monitoreo, Psicologia, Nutricion, Neumologia, Seguimiento, PolisomnografiaBasal, PolisomnografiaTitulacion

# Register your models here.

# Registro del modelo Monitoreo en el admin de Django
@admin.register(Monitoreo)
class MonitoreoAdmin(admin.ModelAdmin):
    list_display = (
        'ingreso',
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
        'ingreso',
        'inventario_depre_beck',
        'inventario_ansiedad_beck',
        'escala_atenas',
        'registrado_por',
        'created_at',
    )
    
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# Registro del modelo Nutricion en el admin de Django
@admin.register(Nutricion)
class NutricionAdmin(admin.ModelAdmin):
    list_display = (
        'ingreso',
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
    
# Registro del modelo Neumologia en el admin de Django
@admin.register(Neumologia)
class NeumologiaAdmin(admin.ModelAdmin):
    list_display = (
        'ingreso',
        'registrado_por',
        'created_at',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    

# Registro del modelo PolisomnografiaBasal en el admin de Django
@admin.register(PolisomnografiaBasal)
class PolisomnografiaBasalAdmin(admin.ModelAdmin):
    list_display = (
        'ingreso',
        'registrado_por',
        'created_at',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    

# Registro del modelo PolisomnografiaTitulacion en el admin de Django
@admin.register(PolisomnografiaTitulacion)
class PolisomnografiaTitulacionAdmin(admin.ModelAdmin):
    list_display = (
        'ingreso',
        'registrado_por',
        'created_at',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


#Registro del modelo Seguimientos en el admin de Django
@admin.register(Seguimiento)
class SeguimientosAdmin(admin.ModelAdmin):
    list_display = (
        'ingreso',
        'fecha_atencion',
        'tipo_servicio',
        'registrado_por',
        'created_at',
    )

    search_fields = (
        'patient__name',
        'registrado_por__username',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
