from django.test import TestCase

import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_cadastro_controller(client):
    dados = {
        "nome": "João",
        "email": "joao@example.com",
        "senha": "123456",
        "tipo": "Cliente",
        "telefone": "11999999999",
        "cidade": "São Paulo",
        "cpf": "123.456.789-00",
        "data_nascimento": "2000-01-01"
    }

    resposta = client.post(
        "/api/cadastro/",  # ou outra URL mapeada
        data=dados,
        content_type="application/json"
    )

    assert resposta.status_code == 200
    body = resposta.json()
    assert body["success"] is True
    assert "sucesso" in body["message"].lower()
