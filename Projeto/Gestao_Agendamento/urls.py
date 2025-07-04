from django.urls import path
from .views import central_view, teste_controller_view

urlpatterns = [
    path('central/', central_view),
    path('', teste_controller_view),  # para abrir o HTML de testes
]
