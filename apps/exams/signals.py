from django.db.models.signals import post_save
from django.dispatch import receiver
# Importa todos tus modelos de exámenes aquí
from .models import Monitoreo, Psicologia, Nutricion, Neumologia, Seguimiento

# Pasamos una lista de modelos al decorador
@receiver(post_save, sender=Monitoreo)
@receiver(post_save, sender=Psicologia)
@receiver(post_save, sender=Nutricion)
@receiver(post_save, sender=Neumologia)
def registro_atencion_unificada(sender, instance, created, **kwargs):
    if created:
        # Verificamos que el examen tenga un ingreso asociado
        if instance.ingreso:
            Seguimiento.objects.create(
                ingreso=instance.ingreso, # El campo en Seguimiento se llama 'ingreso'
                registrado_por=instance.registrado_por,
                tipo_servicio=sender.__name__,
                # Usamos la fecha del examen para la fecha de atención
                fecha_atencion=instance.created_at.date() 
            )