from Projeto import settings
from Projeto.Gestao_Agendamento.gestao_agendamento import *
from ..Login_Autenticacao.views import *
from ..Gestao_Agendamento.views import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import ensure_csrf_cookie



User = get_user_model()

@csrf_exempt
def processar_requisicao(request):
    try:
        data = json.loads(request.body)
        return data
    except json.JSONDecodeError:
        print("Erro ao processar JSON")
        return JsonResponse(
            {"success": False, "message": "Json inválido"}, status=400
        )

@csrf_exempt
def login_view(request):
    data = processar_requisicao(request)

    success, msg, user_id, tipo, name, email, cpf, telefone, data_nascimento, cidade = login1(data)

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
    data = cadastro(data)

    return data

@csrf_exempt
def inserir_agendamento_view(request):
    data = processar_requisicao(request)
    return inserir_agendamento_logica(data)

@csrf_exempt
def remover_agendamento_view(request):
    data = processar_requisicao(request)
    return remover_agendamento_logica(data)

@csrf_exempt
def atualizar_agendamento_view(request):
    data = processar_requisicao(request)
    return atualiza_agendamento_logica(data)

@csrf_exempt
def listar_agendamentos_view(request):
    data = processar_requisicao(request)
    return lista_agendamentos_logica(data)

@csrf_exempt
def editar_perfil_view(request, id):    

    if request.method == "DELETE":
        return deletar_perfil(id)
    
    elif request.method == "PUT":
        data = processar_requisicao(request)
        response = editar_perfil(data, id)    
        return response

@csrf_exempt
def cadastro_local_view(request,id):
    status, msg = verifica_local(id)
    if status == False:
        data = processar_requisicao(request)
        return cadastrar_local(data,id)
         
    return JsonResponse({'status':False, 'msg': msg})

@csrf_exempt
def editar_local_view(request,id):
    data = processar_requisicao(request)
    return editar_local(data,id)

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
    response = cadastrar_horario(data, id)
    return response

@csrf_exempt
def forgot_pass_view(request):
    
    email = processar_requisicao(request)
    print(email)
    response = recuperar_senha(email)
    return response

@csrf_exempt
def obtem_local_view(request):
    data = processar_requisicao(request)
    response = obter_local_agendamento_logica(data)
    return response

@csrf_exempt
def prox_agend_view(request):
    data = processar_requisicao(request)
    response = obter_proximo_agendamento_e_local_logica(data)
    return response

@csrf_exempt
def local_barbeiro_view(request):

    response = listar_locais_barbeiro_logica()
    return response

@csrf_exempt
def agenda_barbeiro_view(request):
    data = processar_requisicao(request)
    response = listar_agendamentos_barbeiro_logica(data)
    return response

@csrf_exempt
def recuperar_dados_perfil_view(request,id):
    response = recuperar_dados_perfil(id)
    return response

@csrf_exempt
def recuperar_senha_view(request,id):
    response = recuperar_senha(request, id)
    return response


@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get("token")

        if not token:
            return JsonResponse({"success": False, "message": "Token não fornecido"}, status=400)

        # Verifica o token com o Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
        email = idinfo["email"]
        name = idinfo["name"]
        sub = idinfo["sub"]

        # Verifica se já existe um usuário com este e-mail
        usuario = Usuario.objects.filter(email=email).first()
        
        if not usuario:
            # Cria um novo usuário se não existir
            usuario = Usuario.objects.create(
                email= email,
                senha= "",  # pode deixar em branco ou armazenar o ID do Google, se quiser
            )
       
        r = pos_login(idinfo, usuario.id)
        
        #print("R: ", r)
        # Aqui você pode gerar um token (JWT, etc). Por enquanto, retorna o usuário.
        return JsonResponse({
            "success": True,
            "user": {
                "id": usuario.id,
                "email": usuario.email,
                "tipo": usuario.tipo,
                "id_google": sub,
            }
        })

    except ValueError:
        return JsonResponse({"success": False, "message": "Token inválido"}, status=400)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"detail": "CSRF cookie set"})