from django.contrib import admin

from Projeto.Login_Autenticacao.models import Local, Servicos, Horarios, Agenda

@admin.register(Local)
class Localadmin(admin.ModelAdmin):
    list_display = ('id', 'nome_local', 'endereco', 'cnpj', 'telefone', 'barbeirousuarioid', 'idhorarios', 'idservicos')

@admin.register(Servicos)
class BarbeirServicosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao', 'preco', 'tempo', 'idlocal')

@admin.register(Horarios)
class HorariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'dia_semana', 'hora_inicio', 'hora_fim', 'idlocal')

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'hora', 'idbarbeiro', 'idcliente', 'idservicos')