from django import forms
from .models import Monitoreo, Psicologia, Nutricion

# formulario para registrar Monitoreo
class MonitoreoForm(forms.ModelForm):
    class Meta:
        model = Monitoreo
        exclude = ['patient', 'registrado_por']
        labels = {
            'uso_diario': 'Porcentaje(%) Uso Diario',
            'dias_uso_horas': 'Porcentaje(%) días uso > 4 horas',
            'hipopnea_basal': 'Indice de apneas/hipopneas BASAL',
            'hipopnea_residual': 'Indice de apneas/hipopneas RESIDUAL',
            'presion_ipap': 'Presion Terapéutica IPAP',
            'presion_epap': 'Presion Terapéutica EPAP',
            'modo_ventilatorio': 'Modo Ventilatorio',
            'mascara_cpap': 'Máscara de CPAP',
            'tamano_mascara': 'Tamaño de Máscara',
            'etco2_promedio': 'EtCO2 Promedio',
        }
        widgets = {
            'uso_diario': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_uso_horas': forms.NumberInput(attrs={'class': 'form-control'}),
            'hipopnea_basal': forms.NumberInput(attrs={'class': 'form-control'}),
            'hipopnea_residual': forms.NumberInput(attrs={'class': 'form-control'}),
            'presion_ipap': forms.NumberInput(attrs={'class': 'form-control'}),
            'presion_epap': forms.NumberInput(attrs={'class': 'form-control'}),
            'modo_ventilatorio': forms.Select(attrs={'class': 'form-control'}),
            'mascara_cpap': forms.Select(attrs={'class': 'form-control'}),
            'tamano_mascara': forms.Select(attrs={'class': 'form-control'}),
            'etco2_promedio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
# formulario para registrar Psicologia
class PsicologiaForm(forms.ModelForm):
    class Meta:
        model = Psicologia
        exclude = ['patient', 'registrado_por']
        labels = {
            'inventario_depre_beck': 'Inventario de Depresión de Beck(BDI)',
            'inventario_ansiedad_beck': 'Inventario de Ansiedad de Beck(BAI)',
            'escala_atenas': 'Escala Atenas (1 a 10)',
        }
        widgets = {
            'inventario_depre_beck': forms.NumberInput(attrs={'class': 'form-control'}),
            'inventario_ansiedad_beck': forms.NumberInput(attrs={'class': 'form-control'}),
            'escala_atenas': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
# formulario para registrar Nutricion
class NutricionForm(forms.ModelForm):
    class Meta:
        model = Nutricion
        exclude = ['patient', 'registrado_por']
        labels = {
            'estado_nutricional': 'Estado Nutricional',
            'carbohidratos_pct': 'Carbohidratos',
            'rumiacion': 'Rumiación Nocturna',
            'cafeina': 'Consumo de Cafeína',
        }
        widgets = {
            'estado_nutricional': forms.Select(attrs={'class': 'form-control'}),
            'carbohidratos_pct': forms.NumberInput(attrs={'class': 'form-control'}),
            'rumiacion': forms.Select(attrs={'class': 'form-control'}),
            'cafeina': forms.NumberInput(attrs={'class': 'form-control'}),
        }