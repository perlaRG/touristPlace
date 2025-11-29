from django.urls import path
from . import views

app_name = 'nucleo'

urlpatterns = [
	path('', views.index, name='index'),
	path('ajustes/', views.ajustes, name='ajustes'),
	path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
	path('principal/', views.pantallaPrincipal, name='principal'),
	path('registro/', views.registro, name='registro'),
]

