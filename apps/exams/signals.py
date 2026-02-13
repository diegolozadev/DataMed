from django.db.models.signals import post_save
from django.dispatch import receiver
# Importa todos tus modelos de exámenes aquí
from .models import Monitoreo, Psicologia, Nutricion, Neumologia, Seguimiento, SeguimientoAdaptacion

# Pasamos una lista de modelos al decorador
@receiver(post_save, sender=Monitoreo)
@receiver(post_save, sender=Psicologia)
@receiver(post_save, sender=Nutricion)
@receiver(post_save, sender=Neumologia)
@receiver(post_save, sender=SeguimientoAdaptacion)
def registro_atencion_unificada(sender, instance, created, **kwargs):
    if created and instance.ingreso:
        # Prioridad: Si el modelo tiene 'fecha_consulta', usamos esa. 
        # Si no (como en Monitoreo o Nutrición), usamos created_at.
        if hasattr(instance, 'fecha_consulta'):
            fecha_final = instance.fecha_consulta
        else:
            fecha_final = instance.created_at.date()

        Seguimiento.objects.create(
            ingreso=instance.ingreso,
            registrado_por=instance.registrado_por,
            tipo_servicio=sender.__name__,
            fecha_atencion=fecha_final 
        )