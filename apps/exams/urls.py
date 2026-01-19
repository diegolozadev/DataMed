from django.urls import path
from . import views

urlpatterns = [
    path('patients/<int:patient_id>/clinical/', views.patient_clinical, name='patient_clinical'),
    path('patients/<int:patient_id>/register_monitoreo/', views.register_monitoreo, name='register_monitoreo'),
    path('patients/<int:patient_id>/register_psicologia/', views.register_psicologia, name='register_psicologia'),
    path('patients/<int:patient_id>/register_nutricion/', views.register_nutricion, name='register_nutricion'),
]
