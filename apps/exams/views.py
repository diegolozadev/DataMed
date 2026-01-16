from django.shortcuts import render, get_object_or_404
from .models import Monitoreo
from apps.patients.models import Patient

# Create your views here.

# Vista para ver la historia clinica de cada paciente

def patient_clinical(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    monitoreos = Monitoreo.objects.filter(patient=patient).order_by('-id')
    
    return render(request,'exams/patient_clinical.html',{
        'patient': patient,
        'monitoreos': monitoreos
    })