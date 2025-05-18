from Projeto.Controller import views
from django.urls import path


# teste local
urlpatterns = [
    #    AGENDAMENTO
    path("inserir-agendamento/", views.processar_requisicao, name="inserir_agendamento"),
    path("remover-agendamento/", views.processar_requisicao, name="remover_agendamento"),
    path("atualizar-agendamento/", views.processar_requisicao, name="atualizar_agendamento"),
    path("listar-agendamentos/", views.processar_requisicao, name="listar_agendamentos"),
    
    #    PERFIL
    path("meu-perfil/editar/", views.processar_requisicao, name="editar_perfil"),
    path("meu-perfil/deletar/", views.processar_requisicao, name="deletar_perfil"),
    
    #    LOGIN E CADASTRO
    path("api/cadastro/", views.processar_requisicao, name="api_cadastro"),
    path("api/login/", views.processar_requisicao, name="api_login"),
    path("api/locals/", views.processar_requisicao, name="api_locals"),
]
