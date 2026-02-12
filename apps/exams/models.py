from django.db import models
from django.conf import settings
from apps.patients.models import Patient, Ingreso

# Create your models here.

# Modelo para guardar los datos de monitoreo de un paciente
class Monitoreo(models.Model):
    
    MODOS_VENTILATORIOS = [
        ("CPAP", "CPAP"),
        ("BPAP", "BPAP"),
        ("BPAP ST", "BPAP ST"),
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
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='monitoreos',
        blank=True,
        null=True
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
    dias_uso_horas_4 = models.DecimalField(max_digits=5, decimal_places=2)
    horas_uso_diario = models.DecimalField(max_digits=5, decimal_places=2)
    hipopnea_basal = models.DecimalField(max_digits=5, decimal_places=2, help_text="Copiado de la PSG Basal al momento del registro")
    hipopnea_residual = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_correccion = models.DecimalField(max_digits=5, decimal_places=2, help_text="Calculado automáticamente: ((Basal - Residual) / Basal) * 100" )
    modo_ventilatorio = models.CharField(max_length=20, choices=MODOS_VENTILATORIOS)
    presion_ipap = models.DecimalField(max_digits=5, decimal_places=2)
    presion_epap = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(help_text="Respiraciones por minuto (rpm)", blank=True, null=True)
    mascara_cpap = models.CharField(max_length=20, choices=MASCARAS_CPAP)
    tamano_mascara = models.CharField(max_length=20, choices=TAMANO_MASCARA)
    etco2_promedio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ingreso.paciente.nombre} - {self.modo_ventilatorio} - {self.created_at.date()}"
    
    

# Modelo para guardar los datos de psicologia de un paciente
class Psicologia(models.Model):
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='psicologias',
        blank=True,
        null=True
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
        return f"{self.ingreso.paciente.nombre} - {self.escala_atenas} - {self.created_at.date()}"



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
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='nutriciones',
        blank=True,
        null=True
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
        return f"{self.ingreso.paciente.nombre} - {self.estado_nutricional} - {self.created_at.date()}"
    


# Vista para registrar datos de neumologia
class Neumologia(models.Model):
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso, 
        on_delete=models.CASCADE,
        related_name='neumologias',
        blank=True,
        null=True
    )

    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='neumologias_registradas'
    )
    
    fecha_consulta = models.DateField()
    medico_tratante = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ingreso.paciente.nombre} - Consulta: {self.fecha_consulta}"
    
    
# Modelo para guardar los datos de polisomnografía basal de un paciente
class PolisomnografiaBasal(models.Model):
    
    SEVERIDAD_APNEA = [
        ("LEVE", "Leve"),
        ("MODERADA", "Moderada"),
        ("NORAMAL", "Normal"),
        ("GRAVE", "Grave"),
    ]
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='polisomnografias_basales',
        blank=True,
        null=True
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='polisomnografias_basales_registradas'
    )
    
    fecha_basal = models.DateField()
    iah = models.DecimalField(max_digits=5, decimal_places=2)
    severidad_apnea = models.CharField(choices=SEVERIDAD_APNEA, max_length=50)
    ido = models.DecimalField(max_digits=5, decimal_places=2)
    eficiencia = models.DecimalField(max_digits=5, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Polisomnografía Basal'
        verbose_name_plural = 'Polisomnografías Basales'
    
    def __str__(self):
        return f"{self.ingreso.paciente.nombre} - AHI: {self.severidad_apnea} - {self.fecha_basal}"
    
    
# Modelo para guardar los datos de polisomnografía de tittulación de un paciente
class PolisomnografiaTitulacion(models.Model):
    
    TIPOS_TITULACION = [
        ("CPAP", "CPAP"),
        ("BPAP", "BPAP"),
        ("BPAP ST", "BPAP ST")
    ]
    
    TALLAS_MASCARAS = [
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large")
    ]
    
    TIPOS_MASCARAS = [
        ("PILLOW NASAL", "Pillow nasal"),
        ("NASAL", "Nasal"),
        ("ORONASAL", "Oronasal")
    ]
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='polisomnografias_titulaciones',
        blank=True,
        null=True
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='polisomnografias_titulaciones_registradas'
    )
    
    
    tipo_titulacion = models.CharField(
        choices=TIPOS_TITULACION, 
        max_length=20, 
        null=True, 
        blank=True,
        verbose_name='Tipo de Titulación')
    
    
    fecha_titulacion = models.DateField()
    presion_ipap = models.DecimalField(max_digits=5, decimal_places=2)
    presion_epap = models.DecimalField(max_digits=5, decimal_places=2)
    frecuencia_respiratoria = models.IntegerField(help_text="Respiraciones por minuto (rpm)")
    talla_mascara = models.CharField(choices=TALLAS_MASCARAS, max_length=20, default='No especificado')
    tipo_mascara = models.CharField(choices=TIPOS_MASCARAS, max_length=20, default='No especificado')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Polisomnografía de Titulación'
        verbose_name_plural = 'Polisomnografías de Titulación'
    
    def __str__(self):
        return f"{self.ingreso.paciente.nombre} - Titulación: {self.fecha_titulacion}"
    
    
# Modelo para guardar los datos de equipo médico de un paciente
class EquipoMedico(models.Model):
    
    TIPOS_MASCARAS = [
        ("PILLOW NASAL", "Pillow nasal"),
        ("NASAL", "Nasal"),
        ("ORONASAL", "Oronasal")
    ]
    
    TALLAS_MASCARAS = [
        ("SMALL", "Small"),
        ("MEDIUM", "Medium"),
        ("LARGE", "Large")
    ]
    
    MARCA_EQUIPOS = [
        ("BMC", "BMC"),
        ("RESMED", "ResMed"),
        ("PHILIPS RESPIRONICS", "Philips RespiroNics"),
        ("SEFAN", "Sefan"),
        ("RESVENT", "Resvent"),
        ("CURATIVE", "Curative"),
        ("PRISMA", "Prisma"),
        ("DEVILBIS", "Devilbis")
    ]
    
    MODO_VENTILATORIO = [
        ("CPAP", "CPAP"),
        ("BiPAP", "BiPAP"),
        ("BiPAP ST", "BiPAP ST"),
    ]
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='equipos_medicos',
        blank=True,
        null=True
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_medicos_registrados'
    )
    
    tipo_mascara_eq_medico = models.CharField(choices=TIPOS_MASCARAS, max_length=100)
    referencia_mascara = models.CharField(max_length=100, default='No especificado')
    talla_mascara = models.CharField(choices=TALLAS_MASCARAS, max_length=20)
    marca_equipo = models.CharField(choices=MARCA_EQUIPOS, max_length=100)
    serial_equipo = models.CharField(max_length=100)
    modo_ventilatorio = models.CharField(choices=MODO_VENTILATORIO, max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ingreso.paciente.nombre} - Equipo: {self.marca_equipo} - {self.created_at.date()}"
    
    
# Modelo para guardar los datos de seguimiento de un paciente
class Seguimiento(models.Model):
    
    # Relación con el modelo Ingreso
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        related_name='seguimientos',
        blank=True,
        null=True
    )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seguimientos_registrados'
    )
    
    fecha_atencion = models.DateField()
    tipo_servicio = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'
        ordering = ['-fecha_atencion']
    
    def __str__(self):
        return f"{self.ingreso.paciente.nombre} - Seguimiento: {self.tipo_servicio} - {self.fecha_atencion}"