from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

# Create your views here.

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm
    error_message = "Usuario o contraseña incorrectos."
