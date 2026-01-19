from django.db import models
from django.conf import settings
from apps.patients.models import Patient

# Create your models here.

# Modelo para guardar los datos de monitoreo de un paciente
class Monitoreo(models.Model):
    
    MODOS_VENTILATORIOS = [
        ("CPAP", "CPAP"),
        ("BPAP", "BPAP"),
        ("BPAP ST", "BPAP ST"),
        ("AUTOCPAP", "AUTOCPAP"),
        ("AUTOBPAP", "AUTOBPAP")
    ]
    
    MASCARAS_CPAP = [
        ("PILLOW NASAL", "Pillow nasal"),
        ("NASAL", "Nasal"),
        ("ORONASAL", "Oronasal")
    ]
    
    TAMANO_MASCARA = [
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large")
    ]
    
    # Relación con el modelo Patient
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='monitoreos'
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='monitoreos_registrados'
    )
    
    uso_diario = models.DecimalField(max_digits=5, decimal_places=2)
    dias_uso_horas = models.DecimalField(max_digits=5, decimal_places=2)
    hipopnea_basal = models.DecimalField(max_digits=5, decimal_places=2)
    hipopnea_residual = models.DecimalField(max_digits=5, decimal_places=2)
    presion_ipap = models.DecimalField(max_digits=5, decimal_places=2)
    presion_epap = models.DecimalField(max_digits=5, decimal_places=2)
    modo_ventilatorio = models.CharField(max_length=20, choices=MODOS_VENTILATORIOS)
    mascara_cpap = models.CharField(max_length=20, choices=MASCARAS_CPAP)
    tamano_mascara = models.CharField(max_length=20, choices=TAMANO_MASCARA)
    etco2_promedio = models.DecimalField(max_digits=5, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient} - {self.modo_ventilatorio} - {self.created_at.date()}"
    
    

# Modelo para guardar los datos de psicologia de un paciente
class Psicologia(models.Model):
    
    # Relación con el modelo Patient
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='psicologias'
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='psicologias_registradas'
    )
    
    inventario_depre_beck = models.IntegerField()
    inventario_ansiedad_beck = models.IntegerField()
    escala_atenas = models.IntegerField()
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient} - {self.escala_atenas} - {self.created_at.date()}"



# Modelo para guardar los datos de nutrición de un paciente
class Nutricion(models.Model):
    
    ESTADOS_NUTRICIONALES = [
        ("DESNUTRICIÓN", "Desnutrición"),
        ("EUTRÓFICO", "Eutrófico"),
        ("SOBREPESO", "Sobrepeso"),
        ("OBESIDAD I", "Obesidad I"),
        ("OBESIDAD II", "Obesidad II"),
        ("OBESIDAD III", "Obesidad III"),
    ]
    
    RUMIACIONES = [
        ("SI", "Sí"),
        ("NO", "No"),
    ]
    
    # Relación con el modelo Patient
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='nutriciones'
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nutriciones_registradas'
    )
    
    estado_nutricional = models.CharField(choices=ESTADOS_NUTRICIONALES, max_length=20)
    carbohidratos_pct = models.DecimalField(max_digits=5, decimal_places=2)
    rumiacion = models.CharField(choices=RUMIACIONES, max_length=5)
    cafeina = models.DecimalField(max_digits=5, decimal_places=2)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Nutrición'
        verbose_name_plural = 'Nutriciones'
    
    def __str__(self):
        return f"{self.patient} - {self.estado_nutricional} - {self.created_at.date()}"