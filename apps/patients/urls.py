from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_list, name='patients_list'),
    
    # 1. Crear: No recibe ID, usa la vista de creación
    path('create/', views.create_patient, name='create_patient'),
    
    # 2. Detalle/Editar: Recibe el ID y usa la vista de detalle
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
    
    path('follow', views.followups_manager, name='patients_follow'),
    
    path('ingreso/estado/<int:entry_id>/<str:new_status>/', views.change_status_entry, name='change_status_entry'),
    
    path('ingreso/nuevo/<int:patient_id>/', views.create_new_entry, name='create_new_entry'),
]