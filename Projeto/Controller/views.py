from ..Login_Autenticacao.views import login, cadastro, editar_perfil, deletar_perfil
from ..Gestao_Agendamento.views import (
    inserir_agendamento,
    remover_agendamento,
    atualiza_agendamento,
    lista_agendamentos,
)
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Vale a pena transformar a função processar_requisicao em varias funções?

def processar_requisicao(request):
    if (
        request.method == "POST"
        and request.headers.get("Content-Type") == "application/json"
    ):
        try:
            data = json.loads(request.body)
            return data
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Json inválido"}, status=400
            )

@csrf_exempt
def login_view(request):
    data = processar_requisicao(request)
    if not data:
        return JsonResponse(
            {
                "success": False,
                "message": "Dados não fornecidos",
            }
        )

    success, msg, user_id, tipo, name = login(data)

    if success:
        # Armazenando na sessão
        request.session["usuario_id"] = user_id
        request.session["usuario_tipo"] = tipo
        request.session["usuario_nome"] = name

    return JsonResponse(
        {
            "success": success,
            "message": msg,
            "tipo": tipo,
        }
    )

@csrf_exempt
def cadastro_view(request):
    data = processar_requisicao(request)
    success, msg = cadastro(data)

    return JsonResponse(
        {
            "success": success,
            "message": msg,
        }
    )

@csrf_exempt
def inserir_agendamento_view(request):
    data = processar_requisicao(request)
    return inserir_agendamento(data)

@csrf_exempt
def remover_agendamento_view(request):
    data = processar_requisicao(request)
    return remover_agendamento(data)

@csrf_exempt
def atualizar_agendamento_view(request):
    data = processar_requisicao(request)
    return atualiza_agendamento(data)

@csrf_exempt
def listar_agendamentos_view(request):
    data = processar_requisicao(request)
    return lista_agendamentos(data)