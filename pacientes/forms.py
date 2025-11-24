from django import forms
from .models import Paciente, ConsultaPsicologia, ConsultaNeumologia

# Formulario para crear y actualizar pacientes
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'departameto': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'zona_residencia': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'entidad_salud': forms.Select(attrs={'class': 'form-control'}),
            'tipo_afiliacion': forms.Select(attrs={'class': 'form-control'}),
            'regimen': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        
## Formulario para crear y actualizar consultas de psicología
class ConsultaPsicologiaForm(forms.ModelForm):
    class Meta:
        model = ConsultaPsicologia
        fields = '__all__'
        exclude = ['paciente', 'profesional']  # excluir el campo 'paciente' ya que se asignará en la vista
        widgets = {
            'fecha_consulta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
## Formulario para crear y actualizar consultas de neumología
class ConsultaNeumologiaForm(forms.ModelForm):
    class Meta:
        model = ConsultaNeumologia
        fields = '__all__'
        exclude = ['paciente', 'profesional']  # excluir el campo 'paciente' ya que se asignará en la vista
        widgets = {
            'fecha_consulta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia_cardiaca': forms.TextInput(attrs={'class': 'form-control'}),
        }
