from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Usuarios
import urllib.parse

def registrar_datos(request):
	# Verificamos si el usuario envió datos (Dio clic en Guardar)
	if request.method == 'POST':
		# 1. RECOLECCIÓN: Obtenemos datos del HTML usando los 'name' de los inputs
		# request.POST['nombre_en_el_input_html']
		v_nombre = request.POST['nombre']
		v_email = request.POST['email']
		v_contraseña = request.POST['password']
		v_telefono = request.POST['telefono']
		
		# 2. CREACIÓN: Llenamos el modelo con las variables de arriba
		nuevo_registro = Usuarios(
			nombre=v_nombre,  # campo_modelo = variable_recolectada
			email=v_email,
			contraseña=v_contraseña,
			telefono=v_telefono,
		)
		
		# 3. GUARDADO: Confirmamos la grabación en MySQL
		nuevo_registro.save()
		
		# Redirigimos a la página de inicio de sesión con mensaje de éxito
		mensaje = urllib.parse.quote_plus('cuenta creada satisfactoriamente')
		return redirect(reverse('nucleo:iniciosesion') + f'?mensaje={mensaje}')
	
	# Si el método es GET (solo visita), mostramos el formulario vacío
	return render(request, 'registro.html') 

# Vistas simples que renderizan las plantillas existentes.
def index(request):
	return render(request, 'index.html')


def ajustes(request):
	return render(request, 'ajustes.html')


def iniciosesion(request):
	mensaje = request.GET.get('mensaje')
	return render(request, 'iniciosesion.html', {'mensaje': mensaje})


def pantallaPrincipal(request):
	return render(request, 'pantallaPrincipal.html')


def registro(request):
	return render(request, 'registro.html')


def advertencia(request):
	return render(request, 'advertencia.html')


def error_404(request):
	return render(request, '404.html')