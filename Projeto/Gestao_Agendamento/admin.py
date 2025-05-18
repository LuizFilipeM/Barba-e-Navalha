from django.contrib import admin
from .models import Local, Horarios, Agenda, Servicos

admin.site.register(Local)
admin.site.register(Horarios)
admin.site.register(Agenda)
admin.site.register(Servicos)