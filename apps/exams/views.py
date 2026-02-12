from django.shortcuts import redirect, render, get_object_or_404
from apps.exams.forms import MonitoreoForm, PsicologiaForm, NutricionForm, BasalForm, TitulacionForm, NeumologiaForm, EquipoMedicoForm
from .models import Monitoreo, Psicologia, Nutricion, Neumologia, PolisomnografiaBasal, PolisomnografiaTitulacion, EquipoMedico, Ingreso
from apps.patients.models import Patient
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    else:
        # Si no hay ingreso activo, las listas se van vacías
        monitoreos = sesiones_psicologia = sesiones_nutricion = sesiones_neumologia = \
        basales = titulaciones = equipos_medicos = []

    return render(request, 'exams/patient_clinical.html', {
        'patient': patient,
        'ingreso_actual': ingreso_actual,
        'monitoreos': monitoreos,
        'sesiones_psicologia': sesiones_psicologia,
        'sesiones_nutricion': sesiones_nutricion,
        'sesiones_neumologia': sesiones_neumologia,
        'basales': basales,
        'titulaciones': titulaciones,
        'equipos_medicos': equipos_medicos
    })
    

# Vista para registrar datos de MONITOREO
@login_required
def register_monitoreo(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    # --- LÓGICA PARA RECUPERAR PSG BASAL ---
    # Buscamos la PSG más reciente de este paciente
    psg = PolisomnografiaBasal.objects.filter(ingreso=ingreso_actual).last()
    
    # Extraemos el valor si existe, si no, lo dejamos en 0
    # Ajusta 'iah_total' por el nombre del campo en tu modelo PSG
    valor_basal = psg.iah if psg else 0
    # ---------------------------------------

    if request.method == 'POST':
        form = MonitoreoForm(request.POST)
        if form.is_valid():
            monitoreo = form.save(commit=False)
            monitoreo.ingreso = ingreso_actual 
            monitoreo.patient = patient
            monitoreo.registrado_por = request.user
            monitoreo.save()
            
            messages.success(request, f'Monitoreo registrado para {patient.nombre} {patient.apellido} exitosamente ✅')
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        # Pre-llenamos el formulario con el dato de la PSG
        form = MonitoreoForm(initial={'hipopnea_basal': valor_basal})

    return render(request, 'exams/register_monitoreo.html', {
        'patient': patient,
        'form': form
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
            
            # 3. Asignamos los campos que faltan
            exam.paciente = patient
            exam.ingreso = ingreso_actual # Esto es lo que el Signal está pidiendo a gritos
            exam.registrado_por = request.user
            
            # 4. Ahora sí, guardamos y el Signal funcionará feliz
            exam.save() 
            
            messages.success(request, "Examen de psicología registrado.")
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
            
            # 2. Asignamos el ingreso (esto arregla el historial y el Admin)
            nutricion.ingreso = ingreso_actual 
            
            # 3. Asignamos el resto de datos
            nutricion.patient = patient
            nutricion.registrado_por = request.user
            
            nutricion.save()
            
            messages.success(request, f'Sesión de nutrición registrada para {patient.nombre} exitosamente ✅')
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
            neumologia.patient = patient
            neumologia.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            neumologia.registrado_por = request.user
            neumologia.save()
            messages.success(request, f'Consulta de Neumología registrada para {patient.nombre} exitosamente ✅')
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = NeumologiaForm()
    return render(request, 'exams/register_neumologia.html', {'patient': patient, 'form': form})


# vista para registarr datos de BASAL
@login_required
def register_basal(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = BasalForm(request.POST)
        if form.is_valid():
            basal = form.save(commit=False)
            basal.patient = patient
            basal.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            basal.registrado_por = request.user
            basal.save()
            messages.success(request, f'Polisomnografía Basal registrada para {patient.nombre} exitosamente ✅')
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = BasalForm()
    return render(request, 'exams/register_basal.html', {'patient': patient, 'form': form})



# vista para registarr datos de TITULACIÓN
@login_required
def register_titulacion(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = TitulacionForm(request.POST)
        if form.is_valid():
            titulacion = form.save(commit=False)
            titulacion.patient = patient
            titulacion.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            titulacion.registrado_por = request.user
            titulacion.save()
            messages.success(request, f'Polisomnografía Titulación registrada para {patient.nombre} exitosamente ✅')
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = TitulacionForm()
    return render(request, 'exams/register_titulacion.html', {'patient': patient, 'form': form})


# vista para registarr datos de EQUIPO MÉDICO
@login_required
def register_equipo_medico(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    ingreso_actual = patient.ingresos.filter(estado='ACTIVO').first()

    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST)
        if form.is_valid():
            equipo_medico = form.save(commit=False)
            equipo_medico.patient = patient
            equipo_medico.ingreso = ingreso_actual # <-- ASIGNAR INGRESO
            equipo_medico.registrado_por = request.user
            equipo_medico.save()
            messages.success(request, f'Equipo Médico registrado para {patient.nombre} exitosamente ✅')
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = EquipoMedicoForm()
    return render(request, 'exams/register_equipo_medico.html', {'patient': patient, 'form': form})
