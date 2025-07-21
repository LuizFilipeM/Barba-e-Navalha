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

# Função auxiliar: processa uma requisição e retorna os dados do body em um json
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
    except Exception as e:
        print ("ERROR: ", str(e))

# Função auxiliar para uso de requisições que requerem CSRF Token
@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"detail": "CSRF cookie set"})

# Função de login por email e senha: realiza verificação dos dados de login e, caso sucesso, retorna
# os dados do usuário para o Front
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

# Realiza o cadastro de um usuário no banco de dados
@csrf_exempt
def cadastro_view(request):
    data = processar_requisicao(request)
    return cadastro(data)

# Realiza o processo de cadastro de um agendamento no banco de dados
def inserir_agendamento_view(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            return inserir_agendamento_logica(dados)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
# Realiza o processo de remoção de um agendamento no banco de dados
@csrf_exempt
def remover_agendamento_view(request):
    data = processar_requisicao(request)
    return remover_agendamento_logica(data)

# Realiza o processo de atualização de um agendamento no banco de dados
@csrf_exempt
def atualizar_agendamento_view(request):
    data = processar_requisicao(request)
    return atualiza_agendamento_logica(data)

# Retorna todos os agendamentos de um cliente a partir de seu nome
@csrf_exempt
def listar_agendamentos_view(request):
    if request.method != 'GET':
        return JsonResponse({"status": False, "msg": "Método não permitido"}, status=405)
    
    cliente = request.GET.get('cliente')
    if not cliente:
        return JsonResponse({"status": False, "msg": "Parâmetro 'cliente' é obrigatório"}, status=400)
    
    return lista_agendamentos_logica({'cliente': cliente})

# Realiza o processo de editar o perfil do usuário
@csrf_exempt
def editar_perfil_view(request, id):    

    if request.method == "DELETE":
        return deletar_perfil(id)
    
    elif request.method == "PUT":
        data = processar_requisicao(request)
        response = editar_perfil(data, id)    
        return response

# Realiza o processo de cadastro de uma barbearia
@csrf_exempt
def cadastro_local_view(request,id):
    status, msg = verifica_local(id)
    if status == False:
        data = processar_requisicao(request)
        return cadastrar_local(data,id)
         
    return JsonResponse({'status':False, 'msg': msg})

# Realiza o processo de editar uma barbearia
@csrf_exempt
def editar_local_view(request,id):
    data = processar_requisicao(request)
    return editar_local(data,id)

# Realiza o processo de deletar uma barbearia
@csrf_exempt
def delete_local_view(request,id):
    response = apagar_local(id)
    return response

# Realiza o processo de cadastrar um novo serviço em uma barbearia
@csrf_exempt
def cadastro_servico_view(request, id):
    data = processar_requisicao(request)
    response = cadastrar_servico(data, id)
    return response

# Realiza o cadastro do horário de funcionamento de uma barbearia
@csrf_exempt
def cadastrar_horario_view(request, id):
    data = processar_requisicao(request)
    response = cadastrar_horario(data, id)
    return response

# Realiza o processo de recuperação de senha do usuário
@csrf_exempt
def forgot_pass_view(request):
    email = processar_requisicao(request)
    email = email.get("email")
    return recuperar_senha(email)

# Retorna o local da barbearia de um dado agendamento
@csrf_exempt
def obtem_local_view(request):
    data = processar_requisicao(request)
    return obter_local_agendamento_logica(data)

# Retorna o proximo agendamento de um cliente e as informações sobre o local
@csrf_exempt
def prox_agend_view(request):
    data = processar_requisicao(request)
    response = obter_proximo_agendamento_e_local_logica(data)
    return response

# Retorna todas as barbeairas do banco (A atualiazar)
@csrf_exempt
def local_barbeiro_view(request):
    response = listar_todas_barbearias_logica()
    print("Response: ", response  )
    return response

# Retorna os agendamentos futuro de um barbeiro
@csrf_exempt
def agenda_barbeiro_view(request):
    if request.method != 'GET':
        return JsonResponse({"status": False, "msg": "Método não permitido"}, status=405)
    
    barbeiro_id = request.GET.get('barbeiro_id')
    if not barbeiro_id:
        return JsonResponse({"status": False, "msg": "Parâmetro 'barbeiro_id' é obrigatório"}, status=400)
    
    try:
        barbeiro_id = int(barbeiro_id)
        return lista_agendamentos_barbeiro_logica({'barbeiro_id': barbeiro_id})
    except ValueError:
        return JsonResponse({"status": False, "msg": "ID do barbeiro deve ser um número"}, status=400)

# Retorna todos os dados do usuário baseado no id passado
@csrf_exempt
def recuperar_dados_perfil_view(request,id):
    return recuperar_dados_perfil(id)

# Realiza o login via API google
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
    
# Retorna todos os serviços cadastrados e seu local associado
@csrf_exempt
def listar_todos_servicos_view(request):
    return listar_todos_servicos_logica()

# Retorna todos os horarios cadastrados e seu local associado
@csrf_exempt
def listar_todos_horarios_view(request):
    response = listar_todos_horarios_logica()
    
    return response

# Cria intervalos para o barbeiro
@csrf_exempt
def criar_intervalo_view(request):
    data = processar_requisicao(request)
    return criar_intervalo_logica(data)

# Realiza a edição dos dados de uma barbearia
@csrf_exempt
def editar_local_barbeiro_view(request):
    data = processar_requisicao(request)
    return editar_local_barbeiro_logica(data)

# Realiza a edição dos dados de uma barbearia
@csrf_exempt
def editar_servico_barbeiro_view(request):
    data = processar_requisicao(request)
    return editar_servico_barbeiro_logica(data)

# Realiza a exclusão de um serviço de um barbeiro
@csrf_exempt
def excluir_servico_barbeiro_view(request):
    data = processar_requisicao(request)
    return excluir_servico_barbeiro_logica(data)