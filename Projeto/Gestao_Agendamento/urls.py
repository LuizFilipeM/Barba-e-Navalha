from django.urls import path
from django.conf import settings
from . import views
from django.shortcuts import render

# teste local
"""urlpatterns = [
    # path('', views.render_template, name='home'),
    path("teste/", views.teste_controller, name="teste_controller"),
    path("inserir-agendamento/", views.inserir_agendamento, name="inserir_agendamento"),
    path("remover-agendamento/", views.remover_agendamento, name="remover_agendamento"),
    path(
        "atualizar-agendamento/",
        views.atualiza_agendamento,
        name="atualizar_agendamento",
    ),
    path("listar-agendamentos/", views.lista_agendamentos, name="listar_agendamentos"),
]"""
