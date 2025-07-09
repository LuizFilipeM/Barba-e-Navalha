from Projeto.Controller import views
from django.urls import include, path


# Teste local
urlpatterns = [
    #    AGENDAMENTO
    path("inserir-agendamento/", views.inserir_agendamento_view, name="inserir_agendamento"),
    path("remover-agendamento/", views.remover_agendamento_view, name="remover_agendamento"),
    path("atualizar-agendamento/", views.atualizar_agendamento_view, name="atualizar_agendamento"),
    path("listar-agendamentos/", views.listar_agendamentos_view, name="listar_agendamentos"),
    path("obter-local-agendamentos/", views.obtem_local_view, name="obter_local_agendamentos_id"),
    path("prox-agendamento/", views.prox_agend_view, name="obter_local_agendamentos"),
    path("barbershops/", views.local_barbeiro_view, name="obter_local_barbeiro"),
    path("lista-agenda-barber/", views.agenda_barbeiro_view, name="obter_agenda_barbeiro"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('cadastro-google/', views.cadastro_google, name='cad_g'),
    
    
    #    PERFIL
    path("api/users/<int:id>", views.editar_perfil_view, name="editar_perfil"),
    path("api/users/recover/<int:id>/", views.recuperar_dados_perfil_view, name="recuperar_perfil"),
    #path("api/users/recover-password/<int:id>/", views.recuperar_senha_view, name="recuperar_senha"), Possivelmente não utilizada

    #    LOGIN E CADASTRO
    path("api/cadastro/", views.cadastro_view, name="api_cadastro"),
    path("api/login/", views.login_view, name="api_login"),
    path("locals/<int:id>/", views.cadastro_local_view, name="api_cadastro_local"),
    path("forgotPassword", views.forgot_pass_view, name="api_forgot_password"),
    path("api/google-login/", views.google_login),

    #    SERVIÇO
    path("services/<int:id>/", views.cadastro_servico_view, name="api_cadastro_servico"),
    path("list-services", views.listar_todos_servicos_view, name="api_lista_servico"),
    path("edit-services", views.editar_servico_barbeiro_view, name="api_edita_servico"),
    path("delete-services", views.excluir_servico_barbeiro_view, name="api_delete_servico"),

    #   HORARIOS
    path("schedule/<int:id>/", views.cadastrar_horario_view, name="api_cadastro_horario"),
    path("list-schedule", views.listar_todos_horarios_view, name="api_lista_horarios"),
    path("create-interval", views.criar_intervalo_view, name="api_cria_intervalos"),

    #   LOCAL
    path("local-edit/<int:id>/", views.editar_local_view, name="api_editar_local"), # AVALIZAR QUAL FUNCAO SERÁ USADA AQUI
    path("local-delete/<int:id>/", views.delete_local_view, name="api_deletar_local"),

    #   AUXILIARES
    path("csrf/", views.csrf_token_view, name = 'get_cookie'),
]