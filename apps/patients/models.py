from datetime import date
from django.db import models

# Create your models here.

class Patient(models.Model):
    
    TIPOS_DOCUMENTO = [
        ("RC", "Registro Civil"),
        ("TI", "Tarjeta de Identidad"),
        ("CC", "Cédula de Ciudadanía"),
        ("CE", "Cédula de Extranjería"),
        ("PA", "Pasaporte"),
        ("PE", "Permiso Especial de Permanencia"),
    ]
    
    DEPARTAMENTOS = [
        ("AMAZONAS", "Amazonas"),
        ("ANTIOQUIA", "Antioquia"),
        ("ARAUCA", "Arauca"),
        ("ATLÁNTICO", "Atlántico"),
        ("BOLÍVAR", "Bolívar"),
        ("BOYACÁ", "Boyacá"),
        ("CALDAS", "Caldas"),
        ("CAQUETÁ", "Caquetá"),
        ("CASANARE", "Casanare"),
        ("CAUCA", "Cauca"),
        ("CESAR", "Cesar"),
        ("CHOCÓ", "Chocó"),
        ("CÓRDOBA", "Córdoba"),
        ("CUNDINAMARCA", "Cundinamarca"),
        ("GUAINÍA", "Guainía"),
        ("GUAVIARE", "Guaviare"),
        ("HUILA", "Huila"),
        ("LA GUAJIRA", "La Guajira"),
        ("MAGDALENA", "Magdalena"),
        ("META", "Meta"),
        ("NARIÑO", "Nariño"),
        ("NORTE DE SANTANDER", "Norte de Santander"),
        ("PUTUMAYO", "Putumayo"),
        ("QUINDÍO", "Quindío"),
        ("RISARALDA", "Risaralda"),
        ("SAN ANDRÉS Y PROVIDENCIA", "San Andrés y Providencia"),
        ("SANTANDER", "Santander"),
        ("SUCRE", "Sucre"),
        ("TOLIMA", "Tolima"),
        ("VALLE DEL CAUCA", "Valle del Cauca"),
        ("VAUPÉS", "Vaupés"),
        ("VICHADA", "Vichada"),
    ]
    
    CIUDADES = [
        ("BUCARAMANGA", "Bucaramanga"),
        ("MEDELLÍN", "Medellín"),
        ("BOGOTÁ", "Bogotá"),
        ("CARTAGENA", "Cartagena"),
        ("BARRANQUILLA", "Barranquilla"),
        ("MEDELLÍN", "Medellín"),
        ("BOGOTÁ", "Bogotá"),
        ("CARTAGENA", "Cartagena"),
        ("BARRANQUILLA", "Barranquilla"),
    ]
    
    ENTIDADES_SALUD = [
        ("ECOPETROL", "Ecopetrol"),
        ("SANITAS", "Sanitas"),
    ]
    
    

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=3, choices = TIPOS_DOCUMENTO)
    documento = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")])
    departamento = models.CharField(max_length=100, choices=DEPARTAMENTOS)
    ciudad = models.CharField(max_length=100, choices=CIUDADES)
    zona = models.CharField(max_length=10, choices=[("URBANA", "Urbana"), ("RURAL", "Rural")])
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=20, choices=[("SOLTERO", "Soltero"), ("CASADO", "Casado"), ("UNIÓN LIBRE", "Unión Libre"), ("VIUDO", "Viudo"), ("DIVORCIADO", "Divorciado")])
    entidad_salud = models.CharField(max_length=100, choices=ENTIDADES_SALUD)
    estrato = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")])
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # in meters
    perimetro_abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    cuello = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    medico_remitente = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    diagnostico_clinico = models.TextField(max_length=1000, choices=[("G47.3", "Apnea del Sueño")])
    programa = models.CharField(max_length=100, choices=[("PROGRAMA AOS", "Programa aos"), ("PROGRAMA INSOMNIO", "Programa Insomnio")])
    valor_capita = models.DecimalField(max_digits=10,decimal_places=2, default=259783)
    
    @property
    def ingreso_activo(self):
        # Buscamos el ingreso que esté marcado como ACTIVO
        return self.ingresos.filter(estado='ACTIVO').first()

    @property
    def esta_activo(self):
        # Devuelve True si hay algún ingreso activo
        return self.ingresos.filter(estado='ACTIVO').exists()
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.documento}"


# Modelo para registrar los ingresos de los pacientes
class Ingreso(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('SUSPENDIDO', 'Suspendido'),
        ('TERMINADO', 'Terminado')
    ]

    paciente = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='ingresos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    motivo = models.TextField(blank=True, null=True)

    @property
    def mes_capita(self):
        """Calcula el mes actual del programa (1 al 18)"""
        if not self.fecha_inicio:
            return 0
        
        hoy = date.today()
        # Cálculo de meses transcurridos
        meses = (hoy.year - self.fecha_inicio.year) * 12 + (hoy.month - self.fecha_inicio.month) + 1
        
        if meses < 1: return 1
        if meses > 18: return 18
        return meses
    
    class Meta:
        get_latest_by = 'fecha_inicio' # O 'id'

    def __str__(self):
        return f"Ingreso {self.id} - {self.paciente.nombre} ({self.estado})"