from django import forms
from .models import Monitoreo, Psicologia, Nutricion, PolisomnografiaBasal, PolisomnografiaTitulacion, Neumologia, EquipoMedico, SeguimientoAdaptacion

# formulario para registrar Monitoreo
class MonitoreoForm(forms.ModelForm):
    class Meta:
        model = Monitoreo
        exclude = ['registrado_por', 'ingreso']
        labels = {
            'uso_diario': 'Porcentaje(%) Uso Diario',
            'dias_uso_horas_4': 'Porcentaje(%) días uso > 4 horas',
            'horas_uso_diario': 'Horas de uso diario',
            'hipopnea_basal': 'Indice de apneas BASAL',
            'hipopnea_residual': 'Indice de apneas RESIDUAL',
            'porcentaje_correccion': 'Porcentaje de corrección',
            'modo_ventilatorio': 'Modo Ventilatorio',
            'presion_ipap': 'Presion IPAP',
            'presion_epap': 'Presion EPAP',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria',
            'mascara_cpap': 'Máscara de CPAP',
            'tamano_mascara': 'Tamaño de Máscara',
            'etco2_promedio': 'EtCO2 Promedio',
        }
        widgets = {
            'uso_diario': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_uso_horas_4': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas_uso_diario': forms.NumberInput(attrs={'class': 'form-control'}),
            'modo_ventilatorio': forms.Select(attrs={'class': 'form-control'}),
            'hipopnea_basal': forms.NumberInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly'}),
            'hipopnea_residual': forms.NumberInput(attrs={'class': 'form-control'}),
            'porcentaje_correccion': forms.NumberInput(attrs={'class': 'form-control bg-light fw-bold', 'readonly': 'readonly', 'placeholder': 'Calculando...'}),
            'presion_ipap': forms.NumberInput(attrs={'class': 'form-control'}),
            'presion_epap': forms.NumberInput(attrs={'class': 'form-control'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Respiraciones por minuto (rpm)'},),
            'mascara_cpap': forms.Select(attrs={'class': 'form-control'}),
            'tamano_mascara': forms.Select(attrs={'class': 'form-control'}),
            'etco2_promedio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
# formulario para registrar Psicologia
class PsicologiaForm(forms.ModelForm):
    class Meta:
        model = Psicologia
        exclude = ['registrado_por', 'ingreso']
        labels = {
            'inventario_depre_beck': 'Depresión de Beck',
            'inventario_ansiedad_beck': 'Ansiedad de Beck',
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
        exclude = ['registrado_por', 'ingreso']
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
        
    
 # formulario para registrar Neumologia
class NeumologiaForm(forms.ModelForm):
    class Meta:
        model = Neumologia
        exclude = ['registrado_por', 'ingreso']
        labels = {
            'fecha_consulta': 'Fecha de Consulta',
            'medico_tratante': 'Médico Tratante',
            'especialidad': 'Especialidad'
        }
        widgets = {
            'fecha_consulta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medico_tratante': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'})
        }   
    
        
# formulario para registrar Basal
class BasalForm(forms.ModelForm):
    class Meta:
        model = PolisomnografiaBasal
        exclude = ['registrado_por', 'ingreso']
        labels = {
            'fecha_basal': 'Fecha de Estudio Basal',
            'iah': 'Índice de Apneas (IAH)',
            'severidad_apnea': 'Severidad de Apneas',
            'ido': 'IDO',
            'eficiencia': 'Eficiencia(%)'
        }
        widgets = {
            'fecha_basal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'iah': forms.NumberInput(attrs={'class': 'form-control'}),
            'severidad_apnea': forms.Select(attrs={'class': 'form-control'}),
            'ido': forms.NumberInput(attrs={'class': 'form-control'}),
            'eficiencia': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

# formulario para registrar Titulacion
class TitulacionForm(forms.ModelForm):
    class Meta:
        model = PolisomnografiaTitulacion
        exclude = ['registrado_por', 'ingreso']
        labels = {
            'tipo_titulacion': 'Tipo de Titulación',
            'fecha_titulacion': 'Fecha de Estudio de Titulación',
            'presion_ipap': 'Presión IPAP en Titulación',
            'presion_epap': 'Presión EPAP en Titulación',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria',
            'talla_mascara': 'Talla Mascara',
            'tipo_mascara': 'Tipo Mascara'
        }
        widgets = {
            'tipo_titulacion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_titulacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presion_ipap': forms.NumberInput(attrs={'class': 'form-control'}),
            'presion_epap': forms.NumberInput(attrs={'class': 'form-control'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control'}),
            'talla_mascara': forms.Select(attrs={'class': 'form-control'}),
            'tipo_mascara': forms.Select(attrs={'class': 'form-control'}),
        }
        
        
# formulario para registrar equipo médico
class EquipoMedicoForm(forms.ModelForm):
    class Meta:
        model = EquipoMedico
        exclude = ['registrado_por', 'ingreso']
        labels = {
            'tipo_mascara_eq_medico': 'Tipo de Mascara',
            'referencia_mascara': 'Referencia Mascara',
            'talla_mascara': 'Talla de la Máscara',
            'marca_equipo': 'Marca del Equipo',
            'serial_equipo': 'Serial del Equipo',
            'modo_ventilatorio': 'Modo de Ventilación',
            
        }
        widgets = {
            'tipo_mascara_eq_medico': forms.Select(attrs={'class': 'form-control'}),
            'referencia_mascara': forms.TextInput(attrs={'class': 'form-control'}),
            'talla_mascara': forms.Select(attrs={'class': 'form-control'}),
            'marca_equipo': forms.Select(attrs={'class': 'form-control'}),
            'serial_equipo': forms.TextInput(attrs={'class': 'form-control'}),
            'modo_ventilatorio': forms.Select(attrs={'class': 'form-control'}),
        }

# formulario para registrar notas de seguimiento (adaptación)
class SeguimientoAdaptacionForm(forms.ModelForm):
    class Meta:
        model = SeguimientoAdaptacion
        exclude = ['registrado_por', 'ingreso'] 
        
        labels = {
            'observaciones': 'Notas del Seguimiento / Contacto Telefónico',
        }
          
        widgets = {
            # Corregido: 'observaciones' en minúscula y Textarea para párrafos
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe aquí los detalles del contacto con el paciente...',
                'style': 'resize: none;'
            }),
        }
