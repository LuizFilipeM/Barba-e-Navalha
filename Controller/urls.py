from Controller import Control
from django.urls import path
from django.conf import settings
from . import views
from django.shortcuts import render
# teste local
urlpatterns = [
    path('inserir-agendamento/', Control.processar_requisicao, name='inserir_agendamento'),
    path('remover-agendamento/', Control.processar_requisicao, name='remover_agendamento'),
    path('atualizar-agendamento/', Control.processar_requisicao, name='atualizar_agendamento'),
    path('listar-agendamentos/', Control.processar_requisicao, name='listar_agendamentos'),
    path('cadastro/', Control.processar_requisicao, name='cadastro'),
    path('home/', Control.processar_requisicao, name='home'),
    path('meu-perfil/editar/', Control.processar_requisicao, name='editar_perfil'),
    path('meu-perfil/deletar/', Control.processar_requisicao, name='deletar_perfil'),
    path('logout/', Control.processar_requisicao, name='logout'),
]


