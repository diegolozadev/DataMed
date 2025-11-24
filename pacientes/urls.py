from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('patients_list/', views.patients_list, name='patients_list'),
    path('patient/<int:patient_id>/visits/', views.patient_visits, name='patient_visits'),
    path('patient/<int:patient_id>/psicologia/create/', views.create_psicologia_consultation, name='create_psicologia_consultation'),
    path('patient/<int:patient_id>/neumologia/create/', views.create_neumologia_consultation, name='create_neumologia_consultation'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('create/', views.create_patient, name='create_patient'),
]