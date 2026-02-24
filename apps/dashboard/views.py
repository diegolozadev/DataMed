from django.shortcuts import render
from ..patients.models import Ingreso, Patient
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.core.paginator import Paginator


# Create your views here.
@login_required
def dashboard(request):
    
    """
    Vista para el dashboard del sistema. Muestra estadísticas clave sobre los pacientes activos, el último ingreso registrado, y una lista de pacientes sin seguimiento reciente. Además, incluye una gráfica de distribución por mes capita.
    
    """    
    hoy = timezone.now().date()
    limite = hoy - timezone.timedelta(days=15)
    
    # 1. Total de pacientes activos
    patients = Patient.objects.filter(ingresos__estado='ACTIVO').distinct().count()
    
    # 2. Último paciente (Agregamos select_related para evitar consultas extra en el template)
    last_enter = Patient.objects.filter(ingresos__estado='ACTIVO').select_related().order_by('-ingresos__fecha_inicio').first()
    
    # 3. Lógica de Pacientes sin seguimiento
    pacientes_queryset = Patient.objects.filter(
        ingresos__estado='ACTIVO'
    ).annotate(
        fecha_del_ingreso=Max('ingresos__fecha_inicio'),
        ultima_atencion=Max('ingresos__seguimientos__fecha_atencion')
    ).filter(
        Q(ultima_atencion__lt=limite) |
        Q(ultima_atencion__isnull=True, fecha_del_ingreso__lt=limite)
    ).distinct().order_by('ultima_atencion', 'fecha_del_ingreso')

    total_sin_seguimiento = pacientes_queryset.count()
    
    # Para hacer la grafica de distribución por mes capita, necesitamos contar cuántos ingresos activos hay por cada mes capita.
    
    # 1. Traemos todos los ingresos activos
    ingresos_activos = Ingreso.objects.filter(estado='ACTIVO')

    # 2. Agrupamos manualmente usando un diccionario de Python
    conteos = {}
    for ing in ingresos_activos:
        # Usamos tu property/método mes_capita
        mes = ing.mes_capita 
        if mes:
            conteos[mes] = conteos.get(mes, 0) + 1

    # 3. Ordenamos los datos para que la gráfica no salga desordenada
    # Esto crea listas tipo: ['Mes 1', 'Mes 2'] y [10, 15]
    meses_ordenados = sorted(conteos.keys())
    labels_grafica = [f"Capita {m}" for m in meses_ordenados]
    datos_grafica = [conteos[m] for m in meses_ordenados]

    # --- APLICAMOS PAGINACIÓN AQUÍ ---
    # En el dashboard, 10 por página está bien para que no ocupe todo el espacio
    paginator = Paginator(pacientes_queryset, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/dashboard.html', {
        'patients': patients,
        'last_enter': last_enter,
        'page_obj': page_obj,  # <--- Pasamos el objeto paginado
        'total_sin_seguimiento': total_sin_seguimiento,
        'hoy': hoy,
        'labels_grafica': labels_grafica,
        'datos_grafica': datos_grafica,
    })