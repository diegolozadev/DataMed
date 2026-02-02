from django.urls import path
from . import views

urlpatterns = [
    path('patients/<int:patient_id>/clinical/', views.patient_clinical, name='patient_clinical'),
    path('patients/<int:patient_id>/register_monitoreo/', views.register_monitoreo, name='register_monitoreo'),
    path('patients/<int:patient_id>/register_psicologia/', views.register_psicologia, name='register_psicologia'),
    path('patients/<int:patient_id>/register_nutricion/', views.register_nutricion, name='register_nutricion'),
    path('patients/<int:patient_id>/register_neumologia/', views.register_neumologia, name='register_neumologia'),
    path('patients/<int:patient_id>/register_basal/', views.register_basal, name='register_basal'),
    path('patients/<int:patient_id>/register_titulacion/', views.register_titulacion, name='register_titulacion'),
    path('patients/<int:patient_id>/register_equipo_medico/', views.register_equipo_medico, name='register_equipo_medico'),
]
