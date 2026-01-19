from django.shortcuts import redirect, render, get_object_or_404
from apps.exams.forms import MonitoreoForm, PsicologiaForm, NutricionForm
from .models import Monitoreo, Psicologia, Nutricion
from apps.patients.models import Patient

# Create your views here.

# Vista para ver la historia clinica de cada paciente
def patient_clinical(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    monitoreos = Monitoreo.objects.filter(patient=patient).order_by('-id')
    
    sesiones_psicologia = Psicologia.objects.filter(patient=patient).order_by('-id')
    
    sesiones_nutricion = Nutricion.objects.filter(patient=patient).order_by('-id') 
    
    return render(request,'exams/patient_clinical.html',{
        'patient': patient,
        'monitoreos': monitoreos,
        'sesiones_psicologia': sesiones_psicologia,
        'sesiones_nutricion': sesiones_nutricion
    })
    
    
# Vista para registrar un nuevo monitoreo
def register_monitoreo(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = MonitoreoForm(request.POST)
        if form.is_valid():
            monitoreo = form.save(commit=False)
            monitoreo.patient = patient
            monitoreo.registrado_por = request.user
            monitoreo.save()
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = MonitoreoForm()

    return render(request, 'exams/register_monitoreo.html', {
        'patient': patient,
        'form': form
    })
    
    
# Vista para registrar datos de psicologia
def register_psicologia(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PsicologiaForm(request.POST)
        if form.is_valid():
            psicologia = form.save(commit=False)
            psicologia.patient = patient
            psicologia.registrado_por = request.user
            psicologia.save()
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = PsicologiaForm()
    
    return render(request, 'exams/register_psicologia.html', {
        'patient': patient,
        'form': form
    })
    
    
# Vista para registrar datos de nutricion
def register_nutricion(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = NutricionForm(request.POST)
        if form.is_valid():
            nutricion = form.save(commit=False)
            nutricion.patient = patient
            nutricion.registrado_por = request.user
            nutricion.save()
            return redirect('patient_clinical', patient_id=patient.id)
    else:
        form = NutricionForm()
    
    return render(request, 'exams/register_nutricion.html', {
        'patient': patient,
        'form': form
    })