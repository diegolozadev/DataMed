from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Ingreso
from .forms import PatientForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# Esta vista muestra la lista de pacientes
@login_required
def patients_list(request):
    query = request.GET.get('query_search', '')
    mes_filtro = request.GET.get('mes_filtro', '')
    
    # 1. Filtro base: Solo pacientes que tengan al menos un ingreso con estado 'ACTIVO'
    # Usamos __estado para entrar a la tabla relacionada Ingreso
    patients = Patient.objects.filter(ingresos__estado='ACTIVO').distinct()
    
    # 2. Filtro por nombre o documento (sobre los que ya sabemos que están activos)
    if query:
        patients = patients.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(documento__icontains=query)
        )

    # 3. Filtro por la property "mes_capita"
    if mes_filtro:
        filtered_patients = []
        for p in patients:
            # Aquí usamos tu property ingreso_activo que busca el que dice 'ACTIVO'
            ingreso = p.ingreso_activo 
            if ingreso and str(ingreso.mes_capita) == str(mes_filtro):
                filtered_patients.append(p)
        patients = filtered_patients

    return render(request, 'patients/patients_list.html', {
        'patients': patients,
        'rango_meses': range(1, 19),
        'query': query,
    })

# Esta vista es para crear pacientes
@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            
            # Sacamos la fecha del formulario de paciente
            fecha_ingreso = form.cleaned_data.get('fecha_inicio_programa')
            
            # Si por algún motivo la fecha viene vacía, usamos la de hoy
            if not fecha_ingreso:
                from django.utils import timezone
                fecha_ingreso = timezone.now().date()
            
            # Creación limpia del Ingreso
            Ingreso.objects.create(
                paciente=patient,
                fecha_inicio=fecha_ingreso,
                estado='ACTIVO'
            )
            
            messages.success(request, f"Paciente {patient.nombre} {patient.apellido} creado con éxito.")
            return redirect('patients_list')
    else:
        form = PatientForm()
    
    return render(request, 'patients/create_patient.html', {'form': form})



# Esta vista muestra los detalles de un paciente específico
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            
            # Actualizamos la fecha de ingreso si el usuario la movió
            nueva_fecha = form.cleaned_data.get('fecha_inicio_programa')
            if ingreso_actual:
                ingreso_actual.fecha_inicio = nueva_fecha
                ingreso_actual.save()
            
            messages.success(request, f"Datos del paciente {patient.nombre} {patient.apellido} actualizados con éxito.")
            return redirect('patients_list')
    else:
        # Aquí es donde le "inyectamos" la fecha para que aparezca al cargar
        fecha_previa = ingreso_actual.fecha_inicio.strftime('%Y-%m-%d') if ingreso_actual else None
        
        form = PatientForm(instance=patient, initial={
            'fecha_inicio_programa': fecha_previa
        })

    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'form': form,
        'ingreso_actual': ingreso_actual
    })
    
    
# Esta vista muestra los ingresos de un paciente específico
def followups_manager(request):
    query = request.GET.get("query_search")
    # Traemos a todos (activos e inactivos)
    patients = Patient.objects.all().prefetch_related('ingresos')
    
    if query:
        patients = patients.filter(
            Q(documento__icontains=query) | Q(nombre__icontains=query)
        )
    
    return render(request, 'patients/followups_manager.html', {
        'patients': patients,
        'query': query
    })
  
    
# Esta vista es para cambiar el estado del paciente
@login_required
def change_status_entry(request, entry_id, new_status):
    ingreso = get_object_or_404(Ingreso, id=entry_id)
    
    if request.method == 'POST' and new_status == 'TERMINADO':
        # Capturamos los datos obligatorios de cierre
        ingreso.fecha_fin = request.POST.get('fecha_terminacion')
        ingreso.motivo = request.POST.get('motivo_estado')
        ingreso.estado = 'TERMINADO'
        ingreso.save()
        
        messages.success(request, f"Ciclo de {ingreso.paciente.nombre} finalizado y archivado ✅")
    
    return redirect('patients_follow')

 
# Esta vista es para crear un nuevo ingreso
@login_required
def create_new_entry(request, patient_id):
    # 1. Identificamos al paciente
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # 2. Obtenemos la fecha que el usuario puso en el modal
        fecha = request.POST.get('fecha_inicio')
        
        # 3. SEGURIDAD: Antes de crear, verificamos si ya tiene algo abierto
        # Solo permitimos crear si los anteriores están TERMINADOS
        tiene_ciclo_abierto = patient.ingresos.filter(estado__in=['ACTIVO', 'SUSPENDIDO']).exists()
        
        if tiene_ciclo_abierto:
            messages.error(request, "No se puede iniciar nuevo ciclo: El paciente tiene un proceso pendiente.")
        else:
            # 4. CREAMOS EL NUEVO INGRESO
            # Automáticamente mes_capita será 1 por defecto en el modelo
            Ingreso.objects.create(
                paciente=patient,
                fecha_inicio=fecha,
                estado='ACTIVO'
            )
            messages.success(request, f"¡Nuevo ciclo iniciado para {patient.nombre}!")
            
    return redirect('patients_follow')