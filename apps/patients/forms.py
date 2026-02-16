from django import forms
from .models import Patient, Ingreso

class PatientForm(forms.ModelForm):
    
    # Campor que viene del modelo Ingreso  
    fecha_inicio_programa = forms.DateField(
        label="Fecha ingreso al programa",
        widget=forms.DateInput(
            format='%Y-%m-%d', # <--- Muy importante
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )
    
    class Meta:
        model = Patient
        # CAMBIO CLAVE: En lugar de '__all__', listamos los campos.
        # Esto obliga a Django a incluir el campo extra en el ciclo 'for'
        exclude = ['mes_capita']
        
        fields = [
            'nombre', 'apellido', 'tipo_documento', 'documento', 
            'fecha_nacimiento', 'genero', 'departamento', 'ciudad', 
            'zona', 'telefono', 'celular', 'estado_civil', 
            'entidad_salud', 'estrato', 'peso', 'altura', 
            'perimetro_abdominal', 'cuello', 'medico_remitente', 
            'especialidad', 'diagnostico_clinico', 'programa', 
            'fecha_inicio_programa', 'mes_capita', 'valor_capita'
        ]
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date', 'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'zona': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'entidad_salud': forms.Select(attrs={'class': 'form-control'}),
            'estrato': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En kg'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En metros'}),
            'perimetro_abdominal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En centimetros'}),
            'cuello': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'En centimetros'}),
            'medico_remitente': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'diagnostico_clinico': forms.Select(attrs={'class': 'form-control'}),
            'programa': forms.Select(attrs={'class': 'form-control'}),
            'mes_capita': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_capita': forms.NumberInput(attrs={'class': 'form-control'}),
        }