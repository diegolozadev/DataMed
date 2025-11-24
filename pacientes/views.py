from django.shortcuts import render, redirect
from .models import *
from .forms import PacienteForm, ConsultaPsicologiaForm, ConsultaNeumologiaForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')


## Esta vista maneja el registro de nuevos usuarios
# Utilizando el formulario UserCreationForm de Django metodo GET muestra el formulario y metodo POST procesa el formulario
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm()
    })
    else:
        # validar que las contraseñas coincidan
        if request.POST['password1'] == request.POST['password2']:
            # Utilizar try except para manejar el error de nombre de usuario duplicado, si no hay error crear el usuario y redirigir a la pagina de inicio
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario ya existe'
                })
        # Si las contraseñas no coinciden, volver a mostrar el formulario con un mensaje de error
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Las contraseñas no coinciden'
        })


## Esta vista maneja el cierre de sesión de los usuarios
# Utiliza la función logout de Django y redirige a la página de inicio
def logout_view(request):
    logout(request)
    return redirect('home')


## Esta vista maneja el inicio de sesión de los usuarios
# Utiliza el formulario AuthenticationForm de Django, metodo GET muestra el formulario y metodo POST procesa el formulario
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], 
            password=request.POST['password'])
        
        if user is None:
                return render(request, 'login.html', {
                    'form': AuthenticationForm(),
                    'error': 'El nombre de usuario o la contraseña son incorrectos'
                })
        else:
            login(request, user)
            return redirect('home')
            

## Esta vista muestra la lista de pacientes, pero tiene que estar logueado para verla.
@login_required
def patients_list(request):
    patients = Paciente.objects.all()
    return render(request, 'patients_list.html', {
        'patients': patients})



## Esta vista muestra todas las visitas de un paciente hay que juntar la informacion de las consultas de psicologia y neumologia
@login_required
def patient_visits(request, patient_id):
    patient = Paciente.objects.get(id=patient_id)
    psicologia_consultas = ConsultaPsicologia.objects.filter(paciente=patient)
    neumologia_consultas = ConsultaNeumologia.objects.filter(paciente=patient)
    return render(request, 'patient_visits.html', {
        'patient': patient,
        'psicologia_consultas': psicologia_consultas,
        'neumologia_consultas': neumologia_consultas
    })
    

## Esta vista es para crear una nueva consulta de psicología para un paciente específico
@login_required
def create_psicologia_consultation(request, patient_id):
    patient = Paciente.objects.get(id=patient_id)
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = ConsultaPsicologiaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = patient
            consulta.profesional = request.user
            consulta.save()
            return redirect('patient_visits', patient_id=patient.id)
    else:
        form = ConsultaPsicologiaForm()
    return render(request, 'create_psicologia_consultation.html', {
        'form': form,
        'patient': patient,
        'professional': user
    })


## Esta vista es para crear una nueva consulta de neumología para un paciente específico
@login_required
def create_neumologia_consultation(request, patient_id):
    patient = Paciente.objects.get(id=patient_id)
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = ConsultaNeumologiaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = patient
            consulta.profesional = request.user
            consulta.save()
            return redirect('patient_visits', patient_id=patient.id)
    else:
        form = ConsultaNeumologiaForm()
    return render(request, 'create_neumologia_consultation.html', {
        'form': form,
        'patient': patient,
        'professional': user
    })


## Esta vista permite crear un nuevo paciente
@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_list')
        else:
            return render(request, 'create_patient.html', {
                'form': form,
                'error': 'Por favor corrija los errores del formulario.'
            })

    else:
        form = PacienteForm()
        return render(request, 'create_patient.html', {'form': form})

    

## Esta vista muestra los detalles de un paciente específico
@login_required
def patient_detail(request, patient_id):
    patient = Paciente.objects.get(id=patient_id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=patient) # Se utiliza instance para poder actualizar
        if form.is_valid():
            form.save()
            return redirect('patients_list')
        else:
            return render(request, 'patient_detail.html', {
                'patient': patient,
                'form': form,
                'error': 'Por favor corrija los errores del formulario.'
            })
    else:
        form = PacienteForm(instance=patient)
        return render(request, 'patient_detail.html', {
            'patient': patient,
            'form': form,
        })
