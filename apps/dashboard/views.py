from django.shortcuts import render
from ..patients.models import Patient

# Create your views here.

def dashboard(request):
    
    patients = Patient.objects.all()
    
    last_enter = Patient.objects.order_by('-fecha_ingreso').first()
    
    return render(request, 'dashboard/dashboard.html', {
        'patients': patients,
        'last_enter': last_enter,
    })