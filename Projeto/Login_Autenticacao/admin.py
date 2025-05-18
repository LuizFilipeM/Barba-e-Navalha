from django.contrib import admin

from .models import Usuario, Cliente, Barbeiro

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Barbeiro)