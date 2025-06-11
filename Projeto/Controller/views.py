from ..Login_Autenticacao.views import *
from ..Gestao_Agendamento.views import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processar_requisicao(request):
    
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

    success, msg, user_id, tipo, name, email, cpf, telefone, data_nascimento, cidade = login(data)

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
            "name": name,
            "email": email,
            "cpf": cpf,
            "telefone": telefone,
            "data_nascimento": data_nascimento,
            "cidade": cidade,
            "id": user_id,
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

@csrf_exempt
def editar_perfil_view(request, id):
    data = processar_requisicao(request)

    if request.method == "DELETE":
        return deletar_perfil(id)
    
    elif request.method == "PUT":
        return editar_perfil(data, id)

@csrf_exempt
def cadastro_local_view(request,id):
    response = verifica_local(id)
    response = json.loads(response.content)
    if response['status'] == True:
        data = processar_requisicao(request)
        response = cadastrar_local(data,id)
    return JsonResponse({'status':False, 'msg': "Voce ja possui uma barbearia."})

@csrf_exempt
def delete_local_view(request,id):
    response = apagar_local(id)
    return response

@csrf_exempt
def cadastro_servico_view(request, id):
    data = processar_requisicao(request)
    response = cadastrar_servico(data, id)
    return response

@csrf_exempt
def cadastrar_horario_view(request, id):
    data = processar_requisicao(request)
    print(id)
    response = cadastrar_horario(data, id)
    return response
