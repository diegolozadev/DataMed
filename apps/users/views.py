from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

# Create your views here.

class UserLoginView(LoginView):
    """Vista personalizada para el inicio de sesión de usuarios.
        Usamos un formulario personalizado para manejar la autenticación y mostrar un mensaje de error específico en caso de credenciales incorrectas.
        Usando Class-Based Views (CBV) para una mejor organización y reutilización del código.
    """
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm
    error_message = "Usuario o contraseña incorrectos."
