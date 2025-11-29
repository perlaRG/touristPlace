from django.shortcuts import render

# Vistas simples que renderizan las plantillas existentes.
def index(request):
	return render(request, 'index.html')


def ajustes(request):
	return render(request, 'ajustes.html')


def iniciosesion(request):
	return render(request, 'iniciosesion.html')


def pantallaPrincipal(request):
	return render(request, 'pantallaPrincipal.html')


def registro(request):
	return render(request, 'registro.html')
