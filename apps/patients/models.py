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
    
    MEDICOS_REMITENTES = [
        ("DR. JUAN PÉREZ", "Dr. Juan Pérez"),
        ("DRA. MARÍA GÓMEZ", "Dra. María Gómez"),
    ] 


    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=3, choices = TIPOS_DOCUMENTO)
    documento = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")])
    direccion = models.CharField(max_length=300)
    barrio = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, choices=DEPARTAMENTOS)
    ciudad = models.CharField(max_length=100, choices=CIUDADES)
    zona = models.CharField(max_length=10, choices=[("URBANA", "Urbana"), ("RURAL", "Rural")])
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=20, choices=[("SOLTERO", "Soltero"), ("CASADO", "Casado"), ("UNIÓN LIBRE", "Unión Libre"), ("VIUDO", "Viudo"), ("DIVORCIADO", "Divorciado")])
    ocupacion = models.CharField(max_length=100)
    entidad_salud = models.CharField(max_length=100, choices=ENTIDADES_SALUD)
    estrato = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")])
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
    altura = models.DecimalField(max_digits=4, decimal_places=2)  # in meters
    perimetro_abdominal = models.DecimalField(max_digits=5, decimal_places=2)  # in cm
    cuello = models.DecimalField(max_digits=5, decimal_places=2)  # in cm
    medico_remitente = models.CharField(max_length=100, choices=MEDICOS_REMITENTES)
    especialidad = models.CharField(max_length=100, choices=[("MEDICINA GENERAL", "Medicina General"), ("CARDIOLOGÍA", "Cardiología"), ("NEUMOLOGÍA", "Neumología")])
    diagnostico_clinico = models.TextField(max_length=1000, choices=[("G47.3", "Apnea del Sueño"), ("I10", "Hipertensión Esencial (Primaria)"), ("E66.9", "Obesidad No Especificada")])
    programa = models.CharField(max_length=100, choices=[("PROGRAMA AOS", "Programa aos"), ("PROGRAMA INSOMNIO", "Programa Insomnio")])
    estado = models.CharField(max_length=20, choices=[("ACTIVO", "Activo"), ("INACTIVO", "Inactivo"), ("SUSPENDIDO", "Suspendido")], default="ACTIVO")
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(null=True, blank=True)
    motivo_egreso = models.TextField(max_length=500, null=True, blank=True)
    mes_capita = models.IntegerField()
    valor_capita = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.documento}"