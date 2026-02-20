from django.shortcuts import redirect, render, get_object_or_404
from apps.exams.forms import MonitoreoForm, PsicologiaForm, NutricionForm, BasalForm, TitulacionForm, NeumologiaForm, EquipoMedicoForm, SeguimientoAdaptacionForm
from .models import Monitoreo, Psicologia, Nutricion, Neumologia, PolisomnografiaBasal, PolisomnografiaTitulacion, EquipoMedico, Neumologia, SeguimientoAdaptacion
from apps.patients.models import Patient, Ingreso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

# Create your views here.

# Vista para ver la historia clinica de cada paciente
@login_required
def patient_clinical(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # 1. Buscamos ÚNICAMENTE el ingreso que está activo ahora
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()
    
    if ingreso_actual:
        # 2. Filtramos cada examen por ESE ingreso específico
        # Al usar ingreso=ingreso_actual, si el ciclo es nuevo (Mes 1), estas listas estarán vacías.
        monitoreos = Monitoreo.objects.filter(ingreso=ingreso_actual).order_by('-id')
        sesiones_psicologia = Psicologia.objects.filter(ingreso=ingreso_actual).order_by('-id')
        sesiones_nutricion = Nutricion.objects.filter(ingreso=ingreso_actual).order_by('-id')
        sesiones_neumologia = Neumologia.objects.filter(ingreso=ingreso_actual).order_by('-id')
        basales = PolisomnografiaBasal.objects.filter(ingreso=ingreso_actual).order_by('-id') 
        titulaciones = PolisomnografiaTitulacion.objects.filter(ingreso=ingreso_actual).order_by('-id')
        equipos_medicos = EquipoMedico.objects.filter(ingreso=ingreso_actual).order_by('-id')
        sesiones_neumologia = Neumologia.objects.filter(ingreso=ingreso_actual).order_by('-id')
        seguimientos_adaptacion = SeguimientoAdaptacion.objects.filter(ingreso=ingreso_actual).order_by('-id')
        ultima_cita = ingreso_actual.seguimientos.all().order_by('-created_at').first()
    else:
        # Si no hay ingreso activo, las listas se van vacías
        monitoreos = sesiones_psicologia = sesiones_nutricion = sesiones_neumologia = \
        basales = titulaciones = equipos_medicos =  sesiones_neumologia = seguimientos_adaptacion = []
        ultima_cita = None
        

    return render(request, 'exams/patient_clinical.html', {
        'patient': patient,
        'ingreso_actual': ingreso_actual,
        'ultima_cita': ultima_cita,
        'monitoreos': monitoreos,
        'sesiones_psicologia': sesiones_psicologia,
        'sesiones_nutricion': sesiones_nutricion,
        'sesiones_neumologia': sesiones_neumologia,
        'basales': basales,
        'titulaciones': titulaciones,
        'equipos_medicos': equipos_medicos,
        'sesiones_neumologia': sesiones_neumologia,
        'seguimientos_adaptacion': seguimientos_adaptacion
    })
    

# Vista para registrar datos de MONITOREO
@login_required
def register_monitoreo(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    # --- LÓGICA PSG BASAL ---
    psg = PolisomnografiaBasal.objects.filter(ingreso=ingreso_actual).last()
    valor_basal = psg.iah if psg else 0
    # ------------------------

    # Inicializamos ambos formularios para el GET
    form = MonitoreoForm(initial={'hipopnea_basal': valor_basal})
    seguimiento_form = SeguimientoAdaptacionForm()
    active_tab = 'tecnico' # Por defecto abrimos la técnica

    if request.method == 'POST':
        # ¿Se envió el formulario de Monitoreo Técnico?
        if 'btn_monitoreo' in request.POST:
            form = MonitoreoForm(request.POST)
            if form.is_valid():
                monitoreo = form.save(commit=False)
                monitoreo.ingreso = ingreso_actual 
                monitoreo.registrado_por = request.user
                monitoreo.save()
                messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Adaptación registrada para {patient.nombre} exitosamente'))
                return redirect('patient_clinical', patient_id=patient.id)
            active_tab = 'tecnico'

        # ¿Se envió el formulario de Seguimiento/Contacto?
        elif 'btn_contacto' in request.POST:
            seguimiento_form = SeguimientoAdaptacionForm(request.POST)
            if seguimiento_form.is_valid():
                seguimiento = seguimiento_form.save(commit=False)
                seguimiento.ingreso = ingreso_actual
                seguimiento.registrado_por = request.user
                seguimiento.save()
                messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Nota de contacto registrada para {patient.nombre} exitosamente'))
                return redirect('patient_clinical', patient_id=patient.id)
            active_tab = 'contacto' # Si hay error, que se quede en esta pestaña

    return render(request, 'exams/register_monitoreo.html', {
        'patient': patient,
        'form': form,
        'seguimiento_form': seguimiento_form,
        'active_tab': active_tab
    })
    
# Vista para registrar datos de PSICOLOGIA
@login_required
def register_psicologia(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # 1. Buscamos el ingreso activo del paciente
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = PsicologiaForm(request.POST)
        if form.is_valid():
            # 2. commit=False evita que se guarde de inmediato y se dispare el signal
            exam = form.save(commit=False)
            exam.ingreso = ingreso_actual # Esto es lo que el Signal está pidiendo a gritos
            exam.registrado_por = request.user
            
            # 4. Ahora sí, guardamos y el Signal funcionará feliz
            exam.save() 
            
            messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Consulta de psicología registrada para {patient.nombre} exitosamente'))
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = PsicologiaForm()

    return render(request, 'exams/register_psicologia.html', {'form': form, 'patient': patient})
    
    
# Vista para registrar datos de NUTRICIÓN
@login_required
def register_nutricion(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # 1. Buscamos el ingreso activo (OBLIGATORIO para que no sea huérfano)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()
    
    if request.method == 'POST':
        form = NutricionForm(request.POST)
        if form.is_valid():
            nutricion = form.save(commit=False)
            nutricion.ingreso = ingreso_actual 
            nutricion.registrado_por = request.user
            
            nutricion.save()
            
            messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Consulta de nutrición registrada para {patient.nombre} exitosamente'))
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = NutricionForm()
    
    return render(request, 'exams/register_nutricion.html', {
        'patient': patient,
        'form': form,
        'ingreso_actual': ingreso_actual
    })
    

# vista para registarr datos de NEUMOLOGÍA
@login_required
def register_neumologia(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first() # <-- BUSCAR INGRESO

    if request.method == 'POST':
        form = NeumologiaForm(request.POST)
        if form.is_valid():
            neumologia = form.save(commit=False)
            neumologia.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            neumologia.registrado_por = request.user
            neumologia.save()
            messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Consulta de Neumología registrada para {patient.nombre} exitosamente'))
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = NeumologiaForm()
    return render(request, 'exams/register_neumologia.html', {
        'patient': patient, 
        'form': form
        })


# vista para registarr datos de BASAL
@login_required
def register_basal(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = BasalForm(request.POST)
        if form.is_valid():
            basal = form.save(commit=False)
            basal.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            basal.registrado_por = request.user
            basal.save()
            messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Polisomnografía Basal registrada para {patient.nombre} exitosamente'))
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = BasalForm()
    return render(request, 'exams/register_basal.html', {
        'patient': patient, 
        'form': form
        })


# vista para registarr datos de TITULACIÓN
@login_required
def register_titulacion(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = TitulacionForm(request.POST) # <-- Definimos form aquí para el POST
        if form.is_valid():
            titulacion = form.save(commit=False)
            titulacion.ingreso = ingreso_actual
            titulacion.registrado_por = request.user
            titulacion.save()
            messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Polisomnografía Titulación registrada para {patient.nombre} exitosamente'))
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = TitulacionForm() # <-- Definimos form aquí para el GET

    # Al dejar el render AQUÍ (fuera del else), si el form falla, 
    # se recarga la página mostrando los mensajes de "campo obligatorio".
    return render(request, 'exams/register_titulacion.html', {
        'patient': patient, 
        'form': form
    })


# vista para registarr datos de EQUIPO MÉDICO
@login_required
def register_equipo_medico(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST)
        if form.is_valid():
            equipo_medico = form.save(commit=False)
            equipo_medico.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            equipo_medico.registrado_por = request.user
            equipo_medico.save()
            messages.success(request, mark_safe(f'<i class="fa-solid fa-circle-check"></i> Equipo Médico registrado para {patient.nombre} exitosamente'))
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = EquipoMedicoForm()
    return render(request, 'exams/register_equipo_medico.html', {
        'patient': patient, 
        'form': form})

