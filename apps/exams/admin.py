from django.contrib import admin
from .models import Monitoreo

# Register your models here.

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
