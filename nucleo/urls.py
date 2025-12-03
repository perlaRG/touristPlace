from django.urls import path
from . import views

app_name = 'nucleo'

urlpatterns = [
	path('', views.index, name='index'),
	path('ajustes/', views.ajustes, name='ajustes'),
	path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
	path('principal/', views.pantallaPrincipal, name='principal'),
	path('registro/', views.registrar_datos, name='registrar'),
	# Alias para compatibilidad: algunos templates usan 'nucleo:registro'
	path('registro/', views.registrar_datos, name='registro'),
	path('advertencia/', views.advertencia, name='advertencia'),
	path('404/', views.error_404, name='404'),

]

