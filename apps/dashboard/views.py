from django.shortcuts import render
from ..patients.models import Patient
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q


# Create your views here.
@login_required
def dashboard(request):
    hoy = timezone.now().date()
    limite = hoy - timezone.timedelta(days=15)
    
    # 1. Total de pacientes con al menos un ingreso activo
    patients = Patient.objects.filter(ingresos__estado='ACTIVO').distinct().count()
    
    # 2. Último paciente que ingresó (accediendo a la fecha del Ingreso)
    # Usamos select_related para que no sea pesada la consulta
    last_enter = Patient.objects.filter(ingresos__estado='ACTIVO').order_by('-ingresos__fecha_inicio').first()
    
    # 3. Pacientes sin seguimiento (Lógica de los 30 días)
    pacientes_sin_seguimiento = Patient.objects.filter(
        ingresos__estado='ACTIVO' # Solo nos importan los que están en el programa
    ).annotate(
        # Obtenemos la fecha del ingreso actual para comparar si no hay citas
        fecha_del_ingreso=Max('ingresos__fecha_inicio'),
        ultima_atencion=Max('ingresos__seguimientos__fecha_atencion')
    ).filter(
        # Opción 1: Tiene citas, pero la última es vieja
        Q(ultima_atencion__lt=limite) |
        # Opción 2: No tiene citas y su ingreso actual es viejo
        Q(ultima_atencion__isnull=True, fecha_del_ingreso__lt=limite)
    ).distinct().order_by('ultima_atencion', 'fecha_del_ingreso')
    
    total_sin_seguimiento = pacientes_sin_seguimiento.count()
    
    return render(request, 'dashboard/dashboard.html', {
        'patients': patients, # Enviamos el número
        'last_enter': last_enter,
        'pacientes_sin_seguimiento': pacientes_sin_seguimiento,
        'total_sin_seguimiento': total_sin_seguimiento,
        'hoy': hoy,
    })