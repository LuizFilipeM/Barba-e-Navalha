from django.contrib import admin
from .models import Local, Horarios, Agenda, Servicos

admin.site.register(Local)
admin.site.register(Horarios)
admin.site.register(Servicos)
@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'hora', 'idcliente', 'idservicos', 'idbarbeiro')