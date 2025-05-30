from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.hashers import make_password
import json
from django.http import JsonResponse
from datetime import datetime

# Para envio do email
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
import uuid

#TODO VERIFICAR SE TODOS OS RETORNOS ESTÃO COM JSONRESPONSE

def login(data):
    
    email = data.get("email")
    senha = data.get("password")
    
    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):

            tipo = usuario.tipo  # Cliente ou Barbeiro
            # Buscar o nome do usuário a partir do tipo
            if tipo == "Cliente":
                cliente = Cliente.objects.get(id=usuario.id)
            elif tipo == "Barbeiro":
                cliente = Barbeiro.objects.get(id=usuario.id)
        # tipo, name, email, cpf, telefone, data_nascimento, cidade
            return True, "Login realizado com sucesso!", usuario.id, tipo, cliente.nome, email, cliente.cpf, cliente.telefone, cliente.data_nascimento, cliente.cidade

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
        return False, "Email já cadastrado"

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
    return True, "Cadastro realizado com sucesso!"

## Criei essa função, que será chamada pelo controlador para recuperar os dados do usuario na hora de editar.
def recuperar_dados_perfil(usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)

        if usuario.tipo == 'Cliente':
            perfil = Cliente.objects.get(id=usuario)
        elif usuario.tipo == 'Barbeiro':
            perfil = Barbeiro.objects.get(id=usuario)
        else:
            perfil = None  # Para tipo Admin, por exemplo

        return {
            'status': 'success',
            'usuario': usuario,
            'perfil': perfil
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

def editar_perfil(data, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
        if check_password(data['oldPassword'], usuario.senha):

            if usuario.tipo == 'Cliente':
                perfil = Cliente.objects.get(id=usuario)
            elif usuario.tipo == 'Barbeiro':
                perfil = Barbeiro.objects.get(id=usuario)
            else:
                return {'status': 'error', 'message': 'Tipo de usuário inválido'}

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

            return JsonResponse({'status': 'success'})
        else: return JsonResponse({'status':'senha atual incorreta'})

    except Usuario.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def deletar_perfil(user_id):
    
    try:
        usuario = Usuario.objects.get(id=user_id)

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

        return JsonResponse({'status': 'success'})

    except Usuario.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

## Função, chamada pelo controlador, que vai verificar se ja existe local quando o barbeiro clicar em cadastrar local
def verifica_local(usuario_id):
    try:
        barbeiro = Barbeiro.objects.get(id=usuario_id)
        if Local.objects.filter(barbeirousuarioid=barbeiro).exists():
            return True, "Você já possui um local cadastrado."
        return False, ""
    except Barbeiro.DoesNotExist:
        return False, "Usuário (barbeiro) não encontrado."

def cadastrar_local(data):
    nome_local = data.get('nome_local')
    rua = data.get('rua', '').strip()
    bairro = data.get('bairro', '').strip()
    numero = data.get('numero', '').strip()
    cidade = data.get('cidade', '').strip()
    endereco = f"{rua},{bairro},{numero},{cidade}"
    cnpj = data.get('cnpj')
    telefone = data.get('telefone')
    
    try:
        barbeiro = Barbeiro.objects.get(id=data.get('usuario_id'))  # Assumindo que 'usuario_id' é o ID do Barbeiro
    except Barbeiro.DoesNotExist:
        return False, "Usuário (barbeiro) não encontrado"
    
    # Criando Local
    local = Local(
        nome_local=nome_local,
        endereco=endereco,
        cnpj=cnpj,
        telefone=telefone,
        barbeirousuarioid=barbeiro
    )
    local.save()

    return True, "Cadastro realizado com sucesso!"

## Função que recupera os dados do local, chamada pelo controlador, na hora de editar dados
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

def editar_local(data):
    print("Entrou")
    try:
        print("Buscando usuário...")
        usuario = Usuario.objects.get(id=data['usuario_id'])

        print("Buscando barbeiro...")
        barbeiro = Barbeiro.objects.get(id=usuario)

        print("Buscando local...")
        local = Local.objects.get(barbeirousuarioid=barbeiro)

        print("Atualizando dados...")
        rua = data.get('rua', '').strip()
        bairro = data.get('bairro', '').strip()
        numero = data.get('numero', '').strip()
        cidade = data.get('cidade', '').strip()
        endereco = f"{rua},{bairro},{numero},{cidade}"

        local.nome_local = data['nome']
        local.endereco = endereco
        local.telefone = data['telefone']
        local.save()

        print("Dados salvos com sucesso.")
        return {'status': 'success'}

    except Usuario.DoesNotExist:
        print("Usuário não encontrado.")
        return {'status': 'error', 'message': 'Usuário não encontrado'}
    except Exception as e:
        print("Erro ao editar local:", e)
        return {'status': 'error', 'message': str(e)}

def apagar_local(data):
    usuario_id = data.get('usuario_id')

    try:
        barbeiro = Barbeiro.objects.get(id=usuario_id)
        local = Local.objects.get(barbeirousuarioid=barbeiro)

        if local:
            servicos = Servicos.objects.filter(idlocal=local)
            agendas = Agenda.objects.filter(idservico__in=servicos)
            print(f"Agendas relacionadas: {agendas.count()}")
            agendas.delete()
            servicos.delete()
            Horarios.objects.filter(idlocal=local).delete()
            local.delete()

        return {'status': 'success'}

    except Local.DoesNotExist:
        return {'status': 'error', 'message': 'Local não encontrado'}

    except Barbeiro.DoesNotExist:
        return {'status': 'error', 'message': 'Barbeiro não encontrado'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
def cadastrar_servico(data):
    try:
        barbeiro = Barbeiro.objects.get(id=data.get('usuario_id'))  # Assumindo que 'usuario_id' é o ID do Barbeiro
        local = Local.objects.get(barbeirousuarioid=barbeiro)
    except Barbeiro.DoesNotExist:
        return False, "Usuário (barbeiro) não encontrado"
    
    # Dados Serviço
    nome_servico_list = data.get('nome_servico', [])
    descricao_servico_list = data.get('descricao', [])
    preco_list = data.get('preco', [])
    tempo_list = data.get('tempo_servico', [])

    print("Serviços recebidos:")
    print("Nome:", nome_servico_list)
    print("Descrição:", descricao_servico_list)
    print("Preço:", preco_list)
    print("Tempo:", tempo_list)

    # Criando os serviços
    for nome_servico, descricao_servico, preco, tempo in zip(nome_servico_list, descricao_servico_list, preco_list, tempo_list):
        print(f"Salvando serviço: {nome_servico}, {descricao_servico}, {preco}, {tempo}")
        servico = Servicos(
            nome=nome_servico,
            descricao=descricao_servico,
            preco=preco,
            idlocal=local,  # Relaciona o local
            tempo=tempo
        )
        servico.save()

    return True, "Cadastro realizado com sucesso!"

def cadastrar_horario(data):
    try:
        barbeiro = Barbeiro.objects.get(id=data.get('usuario_id'))  # Assumindo que 'usuario_id' é o ID do Barbeiro
        local = Local.objects.get(barbeirousuarioid=barbeiro)
    except Barbeiro.DoesNotExist:
        return False, "Usuário (barbeiro) não encontrado"
    
    # Dados Horarios
    dias_semana = data.get('dias', [])
    horarios_list = data.get('horarios', [])

    # Criando os horários
    for dia in dias_semana:
        for horario in horarios_list:
            if not horario or horario.strip() in ["", "0"]:
                continue  # ignora horários vazios ou inválidos

            try:
                horario_formatado = datetime.strptime(horario.strip(), '%H:%M').time()
            except ValueError:
                return False, f"Horário inválido: {horario}. Use o formato HH:MM."

            horario_obj = Horarios(
                dia_semana=dia,
                horarios=horario_formatado,
                idlocal=local
            )
            horario_obj.save()

    return True, "Cadastro realizado com sucesso!"

def logout_view(request):
    request.session.flush()  # Limpa todos os dados da sessão
    return redirect('login')  # Redireciona para a página de login