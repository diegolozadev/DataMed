from django.shortcuts import render

# Create your views here.

def patients_list(request):
    return render(request, 'patients/patients_list.html')


def create_patient(request):
    return render(request, 'patients/create_patient.html')