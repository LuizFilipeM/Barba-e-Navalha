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

@csrf_exempt
def processar_requisicao(request):
    if (
        request.method == "POST"
        and request.headers.get("Content-Type") == "application/json"
    ):
        url = request.path
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Json inválido"}, status=400
            )

        if not data:
            return JsonResponse(
                {"success": False, "message": "Dados não fornecidos"},
                status=400,
            )

        # Login e Cadastro
        if url == "/api/login/":
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

        elif url == "/api/cadastro/":
            success, msg = cadastro(data)

            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                }
            )

        elif url == "/editar_perfil/":
            success, msg = editar_perfil(data)
            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                    "redirect_url": "/home" if success else "",
                }
            )

        elif url == "/deletar_perfil/":
            success, msg = deletar_perfil(data)
            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                    "redirect_url": "/home" if success else "",
                }
            )

        # Agendamento
        elif url == "/agendar/":
            success, msg = inserir_agendamento(data)
            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                    "redirect_url": "/home" if success else "",
                }
            )

        elif url == "/atualizar_agendamento/":
            success, msg = atualiza_agendamento(data)
            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                    "redirect_url": "/home" if success else "",
                }
            )

        elif url == "/listar_agendamentos/":
            success, msg = lista_agendamentos(data)
            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                    "redirect_url": "/home" if success else "",
                }
            )

        elif url == "/remover_agendamento/":
            success, msg = remover_agendamento(data)
            return JsonResponse(
                {
                    "success": success,
                    "message": msg,
                    "redirect_url": "/home" if success else "",
                }
            )

    # Caso seja GET, apenas renderiza o formulário normalmente
    return JsonResponse(
        {
            "success": False,
            "message": "Metodo nao suportado",
            "redirect_url":"",
        }
    )
