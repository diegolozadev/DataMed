from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Ingreso
from .forms import PatientForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
# Esta vista muestra la lista de pacientes con filtros de búsqueda y paginación
@login_required
def patients_list(request):
    """
    Vista para mostrar la lista de pacientes con filtros de búsqueda y paginación.
    Permite filtrar por nombre, apellido, documento y mes de capitación.
    
    Además, se implementa paginación para manejar grandes cantidades de datos y evitar que Render se caiga. Se muestran 10 pacientes por página y se mantiene el estado de los filtros al navegar entre páginas.
    
    Se agrega un filtro base para mostrar solo pacientes con ingresos activos, y luego se aplican los filtros adicionales según la consulta del usuario. El filtro de mes capita se maneja a través de una iteración manual para evitar problemas con la propiedad calculada en el modelo.
    
    """
    query = request.GET.get('query_search', '')
    mes_filtro = request.GET.get('mes_filtro', '')
    
    # 1. Filtro base
    patients = Patient.objects.filter(ingresos__estado='ACTIVO').distinct()
    
    # 2. Filtro por nombre o documento
    if query:
        patients = patients.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(documento__icontains=query)
        )

    # 3. Filtro por la property "mes_capita" (Esto lo convierte en lista)
    if mes_filtro:
        filtered_patients = []
        for p in patients:
            ingreso = p.ingreso_activo 
            if ingreso and str(ingreso.mes_capita) == str(mes_filtro):
                filtered_patients.append(p)
        patients = filtered_patients

    # --- NUEVA LÓGICA DE PAGINACIÓN ---
    # Usamos 10 por página para que Render no sufra
    paginator = Paginator(patients, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # ----------------------------------

    return render(request, 'patients/patients_list.html', {
        'page_obj': page_obj,  # <--- Pasamos page_obj en lugar de patients
        'rango_meses': range(1, 19),
        'query': query,
        'mes_filtro': mes_filtro, # añadido para que el select se mantenga
    })


# Esta vista es para crear pacientes
@login_required
def create_patient(request):
    """
    Vista para crear un nuevo paciente. Al crear el paciente, también se crea automáticamente un nuevo ingreso con estado "ACTIVO" y la fecha de inicio que el usuario haya ingresado en el formulario. Si el usuario no ingresa una fecha, se asigna la fecha actual por defecto.
    """
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            
            # Sacamos la fecha del formulario de paciente
            fecha_ingreso = form.cleaned_data.get('fecha_inicio_programa')
            
            # Si por algún motivo la fecha viene vacía, usamos la de hoy
            if not fecha_ingreso:
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
    
    """
    Vista para mostrar los detalles de un paciente específico. Permite editar los datos del paciente y actualizar la fecha de inicio del ingreso activo si el usuario la modifica en el formulario.
    """
    
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
@login_required
def followups_manager(request):
    
    """"
    Vista para mostrar los ingresos de un paciente específico. Permite filtrar por nombre, apellido o documento del paciente. Además, se implementa paginación para manejar grandes cantidades de datos y evitar que Render se caiga.
    
    """
    
    query = request.GET.get("query_search")
    
    # Optimizamos con prefetch_related para no hacer consultas N+1 en el template
    # Ordenamos por nombre para que la paginación sea consistente
    patients_list = Patient.objects.all().prefetch_related('ingresos').order_by('nombre')
    
    if query:
        patients_list = patients_list.filter(
            Q(documento__icontains=query) | Q(nombre__icontains=query) | Q(apellido__icontains=query)
        )
    
    # --- Configuración del Paginador ---
    # 15 o 20 pacientes por página es un buen número para esta gestión
    paginator = Paginator(patients_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'patients/followups_manager.html', {
        'page_obj': page_obj, # Cambiamos 'patients' por 'page_obj'
        'query': query,
        'total_count': patients_list.count() # Útil para mostrar "X resultados encontrados"
    })
    
    
# Esta vista es para cambiar el estado del paciente
@login_required
def change_status_entry(request, entry_id, new_status):
    
    """
    Vista para cambiar el estado de un ingreso específico. Si el nuevo estado es "TERMINADO", se requiere que el usuario ingrese la fecha de terminación y el motivo del cambio de estado. Estos datos se capturan a través de un formulario en la plantilla y se guardan en el modelo Ingreso. Después de actualizar el estado, se muestra un mensaje de éxito y se redirige al usuario a la vista de seguimiento de pacientes.
    
    """
    
    
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
    
    """
    Vista para crear un nuevo ingreso para un paciente específico. Antes de crear un nuevo ingreso, se verifica si el paciente tiene algún ingreso activo o suspendido. Si es así, se muestra un mensaje de error indicando que no se puede iniciar un nuevo ciclo hasta que el proceso pendiente esté terminado. Si no hay procesos pendientes, se crea un nuevo ingreso con el estado "ACTIVO" y la fecha de inicio proporcionada por el usuario en el formulario. Después de crear el nuevo ingreso, se muestra un mensaje de éxito y se redirige al usuario a la vista de seguimiento de pacientes.
    
    """
    
    
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