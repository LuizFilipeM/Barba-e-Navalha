from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.hashers import make_password
import json
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Para envio do email
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
import random
import string
import uuid

          
def login1(data):
    email = data.get('email')
    senha = data.get('password')

    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):
            
            tipo = usuario.tipo  # Cliente ou Barbeiro
            # Buscar o nome do usuário a partir do tipo
            if tipo == 'Cliente':
                cli = Cliente.objects.get(id=usuario.id)
            elif tipo == 'Barbeiro':
                cli = Barbeiro.objects.get(id=usuario.id)

            return True, "Login realizado com sucesso!", usuario.id, tipo, cli.nome, usuario.email, cli.cpf, cli.telefone, cli.data_nascimento, cli.cidade
        
        return False, "Senha incorreta", None, None, None, None, None, None, None, None
    except Usuario.DoesNotExist:
        return False, "Usuario não encontrado", None, None, None, None, None, None, None, None

def cadastro(data):
    nome = data.get('name')
    senha = data.get('password')
    tipo = data.get('tipo')
    telefone = data.get('telefone')
    data_nascimento = data.get('data_nascimento')
    email = data.get('email')
    cidade = data.get('cidade')
    cpf = data.get('cpf')

    # Verifica se login já existe
    if Usuario.objects.filter(email=email).exists():
        return JsonResponse ({"status":False, "msg":"Email já cadastrado"})

    # Criação do usuário (com senha criptografada)
    usuario = Usuario(
        email=email,
        senha=make_password(senha),
        tipo=tipo
    )
    usuario.save()  # Aqui o ID do usuário é gerado automaticamente

    # Criação de registro específico de acordo com o tipo
    if tipo == 'Cliente':
        # Atribuindo o objeto Usuario ao campo id
        cliente = Cliente(
            id=usuario,  # Aqui estamos passando a instância do Usuario
            cpf=cpf,
            nome=nome,
            telefone=telefone,
            data_nascimento=data_nascimento,
            cidade=cidade
        )
        cliente.save()
    
    elif tipo == 'Barbeiro':
        # Atribuindo o objeto Usuario ao campo id
        barbeiro = Barbeiro(
            id=usuario,  # Aqui estamos passando a instância do Usuario
            cpf=cpf,
            nome=nome,
            telefone=telefone,
            data_nascimento=data_nascimento,
            cidade=cidade
        )
        barbeiro.save()

    # Se o cadastro foi bem-sucedido, exibe a mensagem de sucesso e redireciona
    return JsonResponse({"status":True, "msg":"Cadastro realizado com sucesso!"})

def pos_login(data, id_usuario):
    # Verifica se o usuário está autenticado e se o usuario_id existe na sessão
    print("Entrou Pos login")
    
    if id_usuario:
        try:
            
            usuario = Usuario.objects.get(id=id_usuario)
            
            # Se o tipo do usuário já está definido, redireciona para a home
            if usuario.tipo: 
                print("user tem tipo definido")
                return True
            else:
                print("user nao tem tipo definido")
                return redirect("/pos-login")

        except Usuario.DoesNotExist:
            print("Usuario não encontrado")
            return False
    else:
        return False
        
@csrf_exempt
def cadastro_google(data):
    data = json.loads(data.body)
    tipo = data.get('tipo')
    usuario_id = data.get('usuario_id')
    nome = data.get('nome_google')
    telefone = data.get('telefone')
    data_nascimento = data.get('data_nascimento')
    cidade = data.get('cidade')
    cpf = data.get('cpf')
    
    usuario = Usuario.objects.get(id=84)
    usuario.tipo = tipo
    usuario.save()

    # Cria o perfil correspondente
    if tipo == 'Cliente':
        cliente = Cliente(
            nome=nome,
            id=usuario,
            cpf=cpf,
            telefone=telefone,
            data_nascimento=data_nascimento,
            cidade=cidade
        )
        cliente.save()

        return JsonResponse ({"status":True, "msg":"Cadastro realizado com sucesso!"})

    elif tipo == 'Barbeiro':
        barbeiro = Barbeiro(
            id=usuario,
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            data_nascimento=data_nascimento,
            cidade=cidade
        )
        barbeiro.save()

        return JsonResponse ({"status":True, "msg":"Cadastro realizado com sucesso!"})

    return JsonResponse ({"status":False, "msg":"Erro no cadastro!"})

def gerar_senha_temporaria(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

def recuperar_senha(data):   
    email = data.get('email')
    print(email)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return JsonResponse ({"status": False, "msg": "Email não encontrado"})

    nova_senha = gerar_senha_temporaria()
    usuario.senha = make_password(nova_senha)
    usuario.save()

    if usuario.tipo == "Cliente":
        cliente = Cliente.objects.get(id=usuario.id)
        nome = cliente.nome
    elif usuario.tipo == "Barbeiro":
        barbeiro = Barbeiro.objects.get(id=usuario.id)
        nome = barbeiro.nome
    else:
        return JsonResponse ({"status": False, "msg": "Tipo invalido"})

    subject = 'Nova Senha Temporária'
    message = render_to_string('emails/reset_email.html', {
        'nome': nome,
        'nova_senha': nova_senha,
    })
    send_mail(subject, message, None, [usuario.email])

    return JsonResponse ({"status": True, "msg": "Uma nova senha foi enviada para seu e-mail."})

def recuperar_dados_perfil(usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)

        if usuario.tipo == 'Cliente':
            perfil = Cliente.objects.get(id=usuario)
        elif usuario.tipo == 'Barbeiro':
            perfil = Barbeiro.objects.get(id=usuario)
        else:
            perfil = None  # Para tipo Admin, por exemplo
        return JsonResponse({
            "status": True,
            "id": usuario.id,
            "tipo": usuario.tipo,
            "email": usuario.email,
            "nome": perfil.nome,
            "telefone": perfil.telefone,
            "cidade": perfil.cidade,
            "data_nascimento": perfil.data_nascimento,
            "cpf": perfil.cpf,
        })

    except Usuario.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Usuário não encontrado"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

def editar_perfil(data, id):
    senha = data.get('oldPassword')
    print(senha)
    try:
        usuario = Usuario.objects.get(id=id)
        if check_password(senha, usuario.senha):
            print("AQUI3    ")  

            if usuario.tipo == 'Cliente':
                perfil = Cliente.objects.get(id=usuario)
            elif usuario.tipo == 'Barbeiro':
                perfil = Barbeiro.objects.get(id=usuario)
            else:
                return JsonResponse ({'status': 'error', 'msg': 'Tipo de usuário inválido'})

            # Atualiza o usuário
            usuario.email = data['email']
            if data['newPassword']:
                usuario.senha = make_password(data['newPassword'])
            usuario.save()

            # Atualiza o perfil
            perfil.nome = data['name']
            perfil.telefone = data['telefone']
            perfil.cidade = data['cidade']
            perfil.save()

            print("AQUI2")
            return JsonResponse ({'status': 'success'})
        
        else:
            return JsonResponse ({'status': 'error', 'message': 'Senha incorreta'})

    except Usuario.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Usuário não encontrado'})
    except Exception as e:
        return JsonResponse ({'status': 'error', 'message': str(e)})

def deletar_perfil(id):
    
    try:
        usuario = Usuario.objects.get(id=id)

        if usuario.tipo == 'Cliente':
            cliente = Cliente.objects.get(id=usuario)
            Agenda.objects.filter(idcliente=cliente).delete()
            cliente.delete()

        elif usuario.tipo == 'Barbeiro':
            barbeiro = Barbeiro.objects.get(id=usuario)
            Agenda.objects.filter(idbarbeiro=barbeiro).delete()
            locais = Local.objects.filter(barbeirousuarioid=barbeiro)
            for local in locais:
                Servicos.objects.filter(idlocal=local).delete()
                Horarios.objects.filter(idlocal=local).delete()
                local.delete()

            barbeiro.delete()

        usuario.delete()

        return JsonResponse ({'status': 'success'})

    except Usuario.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Usuário não encontrado'})
    except Exception as e:
        return JsonResponse ({'status': 'error', 'message': str(e)})

def verifica_local(usuario_id):
    try:
        barbeiro = Barbeiro.objects.get(id=usuario_id)
        if Local.objects.filter(barbeirousuarioid=barbeiro).exists():
            return True, "Você já possui um local cadastrado."
        return False, ""
    except Barbeiro.DoesNotExist:
        return True, "Usuário (barbeiro) não encontrado."

def cadastrar_local(data, id):
    nome_local = data.get('nomeLocal')
    rua = data.get('rua', '').strip()
    bairro = data.get('bairro', '').strip()
    numero = data.get('numero', '').strip()
    cidade = data.get('cidadeLocal', '').strip()
    endereco = f"{rua},{bairro},{numero},{cidade}"
    cnpj = data.get('cnpj')
    telefone = data.get('telefone')
    
    try:
        barbeiro = Barbeiro.objects.get(id=id)
    except Barbeiro.DoesNotExist:
        return JsonResponse ({"status": False, "msg": "Usuário (barbeiro) não encontrado"})
    
    # Criando Local
    local = Local(
        nome_local=nome_local,
        endereco=endereco,
        cnpj=cnpj,
        telefone=telefone,
        barbeirousuarioid=barbeiro
    )
    local.save()

    return JsonResponse ({"status": True, "msg": "Cadastro realizado com sucesso!"})

def recuperar_dados_local(usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        barbeiro = Barbeiro.objects.get(id=usuario)

        if barbeiro:
            local = Local.objects.get(barbeirousuarioid=barbeiro)
        else:
            local = None  # Para tipo Admin, por exemplo

        return {
            'status': 'success',
            'usuario': usuario,
            'local': local
        }

    except Usuario.DoesNotExist:
        return {
            'status': 'error',
            'message': 'Usuário não encontrado'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def editar_local(data, id):
    try:
        print("Buscando usuário...")
        usuario = Usuario.objects.get(id=id)

        print("Buscando barbeiro...")
        barbeiro = Barbeiro.objects.get(id=usuario)

        print("Buscando local...")
        local = Local.objects.get(barbeirousuarioid=barbeiro)

        print("Atualizando dados...")
        rua = data.get('rua', '').strip()
        bairro = data.get('bairro', '').strip()
        numero = data.get('numero', '').strip()
        cidade = data.get('cidadeLocal', '').strip()
        endereco = f"{rua},{bairro},{numero},{cidade}"

        print(data)
        local.nome_local = data['nomeLocal']
        local.endereco = endereco
        local.telefone = data['telefone']
        local.save()

        print("Dados salvos com sucesso.")
        return JsonResponse ({'status': 'success'})

    except Usuario.DoesNotExist:
        print("Usuário não encontrado.")
        return JsonResponse ({'status': 'error', 'message': 'Usuário não encontrado'})
    except Exception as e:
        print("Erro ao editar local:", e)
        return JsonResponse ({'status': 'error', 'message': str(e)})

def apagar_local(id):
    usuario_id = id

    try:
        barbeiro = Barbeiro.objects.get(id=usuario_id)
        local = Local.objects.filter(barbeirousuarioid=barbeiro).first()

        if local:
            servicos = Servicos.objects.filter(idlocal=local)

            agendas = Agenda.objects.filter(idservicos__in=servicos)
            
            print(f"Agendas relacionadas: {agendas.count()}")
            agendas.delete()
            servicos.delete()
            Horarios.objects.filter(idlocal=local).delete()
            local.delete()

        return JsonResponse ({'status': 'success'})

    except Local.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Local não encontrado'})

    except Barbeiro.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Barbeiro não encontrado'})

    except Exception as e:
        return JsonResponse ({'status': 'error', 'message': str(e)})
    
def cadastrar_servico(data, id):
    try:
        barbeiro = Barbeiro.objects.get(id=id)  # Assumindo que 'usuario_id' é o ID do Barbeiro
        local = Local.objects.get(barbeirousuarioid=barbeiro)
    except Barbeiro.DoesNotExist:
        return JsonResponse ({"status": False, "msg": "Usuário (barbeiro) não encontrado"})
    
    # Dados Serviço
    nome_servico = data.get('nomeServico')
    descricao_servico = data.get('descricao')
    preco = data.get('preco')
    tempo = data.get('duracao')

   

    # Criando os serviços
    
    print(f"Salvando serviço: {nome_servico}, {descricao_servico}, {preco}, {tempo}")
    servico = Servicos(
        nome=nome_servico,
        descricao=descricao_servico,
        preco=preco,
        idlocal=local,  
        tempo=tempo
    )
    servico.save()

    return JsonResponse ({"status": True, "msg": "Cadastro realizado com sucesso!"})

def cadastrar_horario(data, id):
    try:
        barbeiro = Barbeiro.objects.get(id=id)  
        local = Local.objects.get(barbeirousuarioid=barbeiro)
    except Barbeiro.DoesNotExist:
        return JsonResponse ({"status": False, "msg": "Usuário (barbeiro) não encontrado"})
    
    # Dados Horarios
    
    horarios_list = data.get('horarios', [])
    

    # Criando os horários
    for dia in horarios_list:
     #   if not horarios_list[dia] or horarios_list[dia].strip() in ["", "0"]:
      #      continue  # ignora horários vazios ou inválidos

        try:
            hora_inicio = datetime.strptime(horarios_list[dia]['horaInicio'].strip(), '%H:%M').time()
            hora_fim = datetime.strptime(horarios_list[dia]['horaFim'].strip(), '%H:%M').time()
            
        except ValueError:
            return JsonResponse ({"status": False, "msg": f"Horário inválido: {dia}. Use o formato HH:MM."})
        
        horario_obj = Horarios(
            dia_semana=dia,
            hora_inicio = hora_inicio,
            hora_fim = hora_fim,
            idlocal = local
            
        )
        horario_obj.save()

    return JsonResponse ({"status": True, "msg": "Cadastro realizado com sucesso!"})

