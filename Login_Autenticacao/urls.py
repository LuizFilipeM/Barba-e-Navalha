from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home_view, name='home'),
    path('meu-perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('meu-perfil/deletar/', views.deletar_perfil_view, name='deletar_perfil'),
    path('logout/', views.logout_view, name='logout'),
]