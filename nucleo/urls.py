from django.urls import path
from . import views

app_name = 'nucleo'
#Urls creadas por Darely
urlpatterns = [
	path('', views.index, name='index'),
	path('ajustes/', views.ajustes, name='ajustes'),
	path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
	path('principal/', views.pantallaPrincipal, name='principal'),
	path('registro/', views.registrar_datos, name='registrar'),
	path('registro-alias/', views.registrar_datos, name='registro'),
	path('advertencia/', views.advertencia, name='advertencia'),
	path('404/', views.error_404, name='404'),
	path('usuarios/', views.usuarios_list, name='usuarios_list'),
	path('editar/<int:id>/', views.editar_usuario, name='editar'),
	path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar'),

]

