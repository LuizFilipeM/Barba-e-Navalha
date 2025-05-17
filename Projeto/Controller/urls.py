from Projeto.Controller import Control
from django.urls import path


# teste local
urlpatterns = [
    path(
        "inserir-agendamento/", Control.processar_requisicao, name="inserir_agendamento"
    ),
    path(
        "remover-agendamento/", Control.processar_requisicao, name="remover_agendamento"
    ),
    path(
        "atualizar-agendamento/",
        Control.processar_requisicao,
        name="atualizar_agendamento",
    ),
    path(
        "listar-agendamentos/", Control.processar_requisicao, name="listar_agendamentos"
    ),
    path("meu-perfil/editar/", Control.processar_requisicao, name="editar_perfil"),
    path("meu-perfil/deletar/", Control.processar_requisicao, name="deletar_perfil"),
    path("api/cadastro/", Control.processar_requisicao, name="api_cadastro"),
    path("api/login/", Control.processar_requisicao, name="api_login"),
]
