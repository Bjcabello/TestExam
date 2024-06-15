from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_sesion, name='login'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registrarse/', views.registro, name='registrarse'),
    path('cuestionario/', views.vista_cuestionario, name='vista_cuestionario'),
    path('resultados/', views.vista_resultados, name='vista_resultados'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]