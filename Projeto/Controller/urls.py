from Projeto.Controller import views
from django.urls import path


# Teste local
urlpatterns = [
    #    AGENDAMENTO
    path("inserir-agendamento/", views.inserir_agendamento_view, name="inserir_agendamento"),
    path("remover-agendamento/", views.remover_agendamento_view, name="remover_agendamento"),
    path("atualizar-agendamento/", views.atualizar_agendamento_view, name="atualizar_agendamento"),
    path("listar-agendamentos/", views.listar_agendamentos_view, name="listar_agendamentos"),

    #    PERFIL
    path("api/users/<int:id>", views.editar_perfil_view, name="editar_perfil"),

    #    LOGIN E CADASTRO
    path("api/cadastro/", views.cadastro_view, name="api_cadastro"),
    path("api/login/", views.login_view, name="api_login"),
    path("locals/<int:id>/", views.cadastro_local_view, name="api_cadastro_local"),
    #path("forgotPassword", views.forgot_password_view, name="api_cforgot_password"),

    #    SERVIÇO
    path("services/<int:id>/", views.cadastro_servico_view, name="api_cadastro_servico"),

    #HORARIOS
    path("schedule/<int:id>/", views.cadastrar_horario_view, name="api_cadastro_horario"),
    
]

# cadastro local, serviço e horario