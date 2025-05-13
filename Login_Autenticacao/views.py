from .models import *
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.hashers import make_password
import json

def login(data):
    email = data.get('email')
    senha = data.get('senha')

    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):
            return True, "Login realizado com sucesso!", usuario.id
        return False, "Senha incorreta", None
    except Usuario.DoesNotExist:
        return False, "Usuario não encontrado", None

def cadastro(data):
    nome = data.get('nome')
    senha = data.get('senha')
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

def editar_perfil(data):
    try:
        usuario = Usuario.objects.get(id=data['usuario_id'])

        perfil = None
        if usuario.tipo == 'Cliente':
            perfil, _ = Cliente.objects.get_or_create(id=usuario)
        elif usuario.tipo == 'Barbeiro':
            perfil, _ = Barbeiro.objects.get_or_create(id=usuario)

        usuario.email = data['email']
        nova_senha = data['senha']
        if nova_senha:
            usuario.senha = make_password(nova_senha)
        usuario.save()

        perfil.nome = data['nome']
        perfil.telefone = data['telefone']
        perfil.cidade = data['cidade']
        perfil.save()

        return {'status': 'success'}
    
    except Usuario.DoesNotExist:
        return {'status': 'error', 'message': 'Usuário não encontrado'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def deletar_perfil(data):
    try:
        usuario = Usuario.objects.get(id=data['usuario_id'])

        perfil = None
        if usuario.tipo == 'Cliente':
            perfil = Cliente.objects.get(id=usuario)
            perfil.delete()
        elif usuario.tipo == 'Barbeiro':
            perfil = Barbeiro.objects.get(id=usuario)
            perfil.delete()

        usuario.delete()

        return {'status': 'success'}
    
    except Usuario.DoesNotExist:
        return {'status': 'error', 'message': 'Usuário não encontrado'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}