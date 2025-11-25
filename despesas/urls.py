from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_despesas, name='lista_despesas'),
    path('adicionar/', views.criar_despesa, name='criar_despesa'),
    # Novas rotas:
    path('editar/<int:pk>/', views.editar_despesa, name='editar_despesa'),
    path('excluir/<int:pk>/', views.excluir_despesa, name='excluir_despesa'),
    path('registro/', views.registro, name='registro'),
]