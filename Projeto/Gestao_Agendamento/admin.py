from django.contrib import admin

from Projeto.Login_Autenticacao.models import *



@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'hora', 'idbarbeiro', 'idcliente', 'idservicos')

@admin.register(Horarios)
class HorariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'dia_semana', 'hora_inicio', 'hora_fim')

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_local', 'endereco', 'cnpj', 'telefone', 'idservicos', 'idhorarios', 'barbeirousuarioid')

@admin.register(Servicos)
class SericosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao', 'preco', 'tempo', 'idlocal')