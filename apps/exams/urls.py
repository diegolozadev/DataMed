from django.urls import path
from . import views

urlpatterns = [
    path('patients/<int:patient_id>/clinical/', views.patient_clinical, name='patient_clinical')
]
