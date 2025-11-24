from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Modelo para almacenar la información de los pacientes
class Paciente(models.Model):
    tipo_documento = models.CharField(
        max_length=10,
        choices=[
            ('ASC', 'Adulto Sin Documento'),
            ('CC', 'Cédula de Ciudadanía'),
            ('CE', 'Cédula de Extranjería'),
            ('MSC', 'Menor de Edad Sin Documento'),
            ('NUIP', 'Número Único de Identificación Personal'),
            ('PAS', 'Pasaporte'),
            ('RC', 'Registro Civil'),
            ('TI', 'Tarjeta de Identidad'),
            ('PPT', 'Permiso de Permanencia Temporal'),
        ]
    )
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(
        max_length=10,
        choices=[
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro'),
        ]
    )
    direccion = models.CharField(max_length=255)
    barrio = models.CharField(max_length=200)
    departameto = models.CharField(
        max_length=100,
        choices=[
            ('AMAZONAS', 'Amazonas'),
            ('ANTIOQUIA', 'Antioquia'),
            ('ARAUCA', 'Arauca'),
            ('ATLANTICO', 'Atlántico'),
            ('BOGOTA', 'Bogotá D.C.'),
            ('BOLIVAR', 'Bolívar'),
            ('BOYACA', 'Boyacá'),
            ('CALDAS', 'Caldas'),
            ('CAQUETA', 'Caquetá'),
            ('CASANARE', 'Casanare'),
            ('CAUCA', 'Cauca'),
            ('CESAR', 'Cesar'),
            ('CHOCO', 'Chocó'),
            ('CORDOBA', 'Córdoba'),
            ('CUNDINAMARCA', 'Cundinamarca'),
            ('GUAINIA', 'Guainía'),
            ('GUAVIARE', 'Guaviare'),
            ('HUILA', 'Huila'),
            ('LA GUAJIRA', 'La Guajira'),
            ('MAGDALENA', 'Magdalena'),
            ('META', 'Meta'),
            ('NARIÑO', 'Nariño'),
            ('NORTE DE SANTANDER', 'Norte de Santander'),
            ('PUTUMAYO', 'Putumayo'),
            ('QUINDIO', 'Quindío'),
            ('RISARALDA', 'Risaralda'),
            ('SAN ANDRES Y PROVIDENCIA', 'San Andrés y Providencia'),
            ('SANTANDER', 'Santander'),
            ('SUCRE', 'Sucre'),
            ('TOLIMA', 'Tolima'),
            ('VALLE DEL CAUCA', 'Valle del Cauca'),
            ('VAUPES', 'Vaupés'),
            ('VICHADA', 'Vichada'),
        ]
    )
    ciudad = models.CharField(max_length=100)
    zona_residencia = models.CharField(
        max_length=10,
        choices=[
            ('RURAL', 'Rural'),
            ('URBANA', 'Urbana'),
        ]
    )
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    estado_civil = models.CharField(
        max_length=15,
        choices=[
            ('SOLTERO', 'Soltero'),
            ('CASADO', 'Casado'),
            ('UNION LIBRE', 'Unión Libre'),
            ('VIUDO', 'Viudo'),
            ('DIVORCIADO', 'Divorciado'),
        ]
    )
    ocupacion = models.CharField(max_length=100)
    entidad_salud = models.CharField(
        max_length=100,
        choices=[
            ('EPS1', 'Entidad Promotora de Salud 1'),
            ('EPS2', 'Entidad Promotora de Salud 2'),
            ('EPS3', 'Entidad Promotora de Salud 3'),
            ('OTRA', 'Otra'),
        ]
    )
    tipo_afiliacion = models.CharField(
        max_length=20,
        choices=[
            ('CONTRIBUTIVO', 'Contributivo'),
            ('SUBSIDIADO', 'Subsidiado'),
            ('VINCULADO', 'Vinculado'),
            ('NINGUNO', 'Ninguno'),
        ]
    )
    regimen = models.CharField(
        max_length=200,
        choices=[
            ('Contributivo Cotizante', 'Contributivo Cotizante'),
            ('Subsidiado', 'Subsidiado'),
        ]
    )
    estado = models.CharField(
        max_length=10,
        choices=[
            ('ACTIVO', 'Activo'),
            ('INACTIVO', 'Inactivo'),
        ]
    )

    def __str__(self):
        return f"{self.nombres}, {self.apellidos}, {self.numero_documento}"
    
    @property
    def edad_actual(self):
        from datetime import date
        today = date.today()
        age = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return age
    
    
## Modelo para almacenar las consultas de psicología de los pacientes
class ConsultaPsicologia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField(auto_now_add=True, )
    motivo_consulta = models.TextField()
    observaciones = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Consulta de Psicología - {self.paciente.nombres} {self.paciente.apellidos} - {self.fecha_consulta}"
    
class ConsultaNeumologia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    motivo_consulta = models.TextField()
    observaciones = models.TextField(blank=True, null=True)
    presion_arterial = models.CharField(max_length=20)
    frecuencia_cardiaca = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Consulta de Neumología - {self.paciente.nombres} {self.paciente.apellidos} - {self.fecha_consulta}"
    

