from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

# Create your views here.

def patients_list(request):
    
    patients = Patient.objects.all()
    
    return render(request, 'patients/patients_list.html', {
        'patients': patients
    })


def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_list')
    else:
        form = PatientForm()

    return render(request, 'patients/create_patient.html', {'form': form})
