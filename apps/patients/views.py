from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm
from django.db.models import Q
from django.contrib import messages

# Create your views here.

# Esta vista muestra la lista de pacientes
def patients_list(request):
    
    patients = Patient.objects.all()
    
    query = request.GET.get("query_search")
    
    if query:
        patients = patients.filter(
            Q(documento__icontains=query) | Q(nombre__icontains=query)
        )
    
    return render(request, 'patients/patients_list.html', {
        'patients': patients,
        'query': query
    })
    

# Esta vista es para crear pacientes
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado exitosamente ✅')
            return redirect('patients_list')
    else:
        form = PatientForm()

    return render(request, 'patients/create_patient.html', {'form': form})


# Esta vista muestra los detalles de un paciente específico
def patient_detail(request, patient_id):
    
    patient = Patient.objects.get(id=patient_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado exitosamente ✅')
            return redirect('patients_list')
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'form': form
    })
