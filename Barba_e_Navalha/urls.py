from django.urls import path
from .views import central_view, teste_controller_view, mostrar_locais_do_barbeiro

urlpatterns = [
    path('central/', central_view),
    path('barbearia/', teste_controller_view),  # para abrir o HTML de testes
    path('barbearia/<int:barbeiro_id>/locais', name="listarLocaisDoBarbeiro", view=mostrar_locais_do_barbeiro),
]
