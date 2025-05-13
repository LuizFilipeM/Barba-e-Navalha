from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    path('meu-perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('meu-perfil/deletar/', views.deletar_perfil, name='deletar_perfil'),
]