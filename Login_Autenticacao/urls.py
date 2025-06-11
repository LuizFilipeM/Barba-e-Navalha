from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('cadastro-google/', views.cadastro_google_view, name='cadastro_google'),
    path('pos-login/', views.pos_login, name='pos_login'),
    path('recuperar-senha', views.recuperar_senha, name='recuperar_senha'),
    path('home/', views.home_view, name='home'),
    path('meu-perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('meu-perfil/deletar/', views.deletar_perfil_view, name='deletar_perfil'),
    path('cadastro-local/', views.cadastrar_local_view, name='cadastro_local'),
    path('meu-local/deletar/', views.apagar_local_view, name='apagar_local'),
    path('meu-local/editar/', views.editar_local_view, name='editar_local'),
    path('cadastro-servicos', views.cadastrar_servico_view, name='cadastro_servicos'),
    path('cadastro-horarios', views.cadastrar_horario_view, name='cadastro_horarios'),
    path('gerenciar-agenda/', views.gerenciar_agenda, name='gerenciar_agenda'),
    path('inserir-agendamentos/', views.inserir_agendamento_view, name='inserir_agendamento'),
    path('ver-agendamentos/', views.ver_agendamentos_view, name='ver_agendamentos'),
    path('logout/', views.logout_view, name='logout'),
]