from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_list, name='patients_list'),
    path('create/', views.create_patient, name='create_patient'),
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
]
