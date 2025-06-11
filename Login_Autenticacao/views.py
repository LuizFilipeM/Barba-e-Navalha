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
import random
import string
import uuid

def login_view(request):
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Json inválido'}, status=400)
        
        success, msg, user_id, tipo, nome = login(data)

        if success:
            # Armazenando na sessão
            request.session['usuario_id'] = user_id
            request.session['usuario_tipo'] = tipo
            request.session['usuario_nome'] = nome

        return JsonResponse({
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        })

    # Caso seja GET, apenas renderiza o formulário normalmente
    return render(request, 'Projeto/login.html')
          
def login(data):
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

def cadastro_view(request):
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)

        success, msg = cadastro(data)

        return JsonResponse({'success': success, 'message': msg})

    # Caso seja GET, apenas renderiza o formulário normalmente
    return render(request, 'Projeto/cadastro.html')

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

def pos_login(request):
    # Verifica se o usuário está autenticado e se o usuario_id existe na sessão
    if request.user.is_authenticated:
        usuario_id = request.session.get('usuario_id')

        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                request.session['usuario_id'] = usuario.id
                request.session['usuario_tipo'] = usuario.tipo
                request.session['usuario_nome'] = request.user.first_name + " " + request.user.last_name

                # Se o tipo do usuário já está definido, redireciona para a home
                if usuario.tipo:
                    return redirect('home')
                else:
                    return redirect('cadastro_google')

            except Usuario.DoesNotExist:
                print("Usuario não encontrado")
                return redirect('login')
        else:
            return redirect('login')
    else:
        return redirect('login')
      
def cadastro_google_view(request):
    # Verifica se o usuário já está autenticado
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Se não tiver usuario_id, redireciona para login

    usuario = Usuario.objects.get(id=usuario_id)

    # Se o usuário já tiver um tipo (Cliente ou Barbeiro), redireciona para home
    if usuario.tipo:
        return redirect('home')

    nome_google = request.user.first_name + " " + request.user.last_name

    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
            data['usuario_id'] = usuario_id
            data['nome_google'] = nome_google
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)

        success, msg = cadastro_google(data)

        return JsonResponse({
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        })

    # Caso seja GET, apenas renderiza o formulário normalmente    
    return render(request, 'Projeto/cadastro_google.html')

def cadastro_google(data):
    tipo = data.get('tipo')
    usuario_id = data.get('usuario_id')
    nome = data.get('nome_google')
    telefone = data.get('telefone')
    data_nascimento = data.get('data_nascimento')
    cidade = data.get('cidade')
    cpf = data.get('cpf')
    
    usuario = Usuario.objects.get(id=usuario_id)
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

def recuperar_senha_view(request):
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Json inválido'}, status=400)
        
        success, msg = recuperar_senha(data)

        if success:
            return JsonResponse({'success': success, 'message': msg})

    # Caso seja GET, apenas renderiza o formulário normalmente
    return render(request, 'Projeto/recuperar_senha.html')

def gerar_senha_temporaria(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

def recuperar_senha(request):   
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'E-mail não encontrado.')
            return redirect('recuperar_senha')

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
            messages.error(request, 'Tipo de usuário inválido.')
            return redirect('recuperar_senha')

        subject = 'Nova Senha Temporária'
        message = render_to_string('emails/reset_email.html', {
            'nome': nome,
            'nova_senha': nova_senha,
        })
        send_mail(subject, message, None, [usuario.email])

        messages.success(request, 'Uma nova senha foi enviada para seu e-mail.')
        return redirect('login')

    return render(request, 'projeto/recuperar_senha.html')

def home_view(request):
    # Recupera os dados da sessão
    usuario_id = request.session['usuario_id']
    tipo = request.session.get('usuario_tipo')
    nome = request.session.get('usuario_nome')

    if not nome or not tipo:
        # Usuário não está logado, redireciona para login
        return redirect('login')

    # Defina ações diferentes dependendo do tipo de usuário
    if tipo == 'Cliente':
        
        acoes = ['Editar Perfil', 'Apagar Perfil', 'Inserir Agendamento', 'Ver Agendamentos']
    elif tipo == 'Barbeiro':
        acoes = ['Editar Perfil', 'Apagar Perfil', 'Cadastrar Local', 'Cadastrar Serviços',
                  'Cadastrar Horarios', 'Editar Local', 'Apagar Local', 'Gerenciar Agenda']
    else:
        acoes = []

    return render(request, 'Projeto/home.html', {
        'nome': nome,
        'tipo': tipo,
        'acoes': acoes,
    })

def editar_perfil_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']

    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        data = json.loads(request.body)
        data['usuario_id'] = usuario_id

        resultado = editar_perfil(data)
        return JsonResponse({'success': resultado['status'] == 'success', 'message': resultado.get('message', '')})

    # Se for GET, busca os dados com a função auxiliar
    resultado = recuperar_dados_perfil(usuario_id)

    if resultado['status'] == 'success':
        return render(request, 'Projeto/usuario_editar_perfil.html', {
            'usuario': resultado['usuario'],
            'perfil': resultado['perfil']
        })
    else:
        return redirect('login')
    
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

def editar_perfil(data):
    senha = data.get('password')
    try:
        usuario = Usuario.objects.get(id=data['usuario_id'])
        if check_password(senha, usuario.senha):

            if usuario.tipo == 'Cliente':
                perfil = Cliente.objects.get(id=usuario)
            elif usuario.tipo == 'Barbeiro':
                perfil = Barbeiro.objects.get(id=usuario)
            else:
                return JsonResponse ({'status': 'error', 'msg': 'Tipo de usuário inválido'})

            # Atualiza o usuário
            usuario.email = data['email']
            if data['password']:
                usuario.senha = make_password(data['password'])
            usuario.save()

            # Atualiza o perfil
            perfil.nome = data['name']
            perfil.telefone = data['telefone']
            perfil.cidade = data['cidade']
            perfil.save()

            return JsonResponse ({'status': 'success'})

    except Usuario.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Usuário não encontrado'})
    except Exception as e:
        return JsonResponse ({'status': 'error', 'message': str(e)})

def deletar_perfil_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']

    if request.method == 'POST':
        data = {'usuario_id': usuario_id}
        resultado = deletar_perfil(data)

        # Logout e redireciona
        request.session.flush()

        if resultado['status'] == 'success':
            return redirect('login')
        else:
            return render(request, 'Projeto/usuario_deletar_perfil.html', {'error': resultado['message']})

    return render(request, 'Projeto/usuario_deletar_perfil.html')

def deletar_perfil(data):
    usuario_id = data.get('usuario_id')
    try:
        usuario = Usuario.objects.get(id=usuario_id)

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

def cadastrar_local_view(request):
    # Recupera o id do usuário logado
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redireciona caso o usuário não esteja logado

    usuario_id = request.session['usuario_id']
    data = {}
    data['usuario_id'] = usuario_id 

    # Se for POST com conteúdo JSON
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            # Carrega os dados JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)
        
        # Adiciona o usuario_id ao JSON data
        data['usuario_id'] = usuario_id

        # Passa o dicionário data para a função de cadastro
        success, msg = cadastrar_local(data)

        # Retorna a resposta com sucesso ou erro
        print("Resultado do cadastro:", success, msg)
        return JsonResponse({
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        })

    # Se for GET, renderiza o formulário
    if request.method == 'GET':
        tem_local, msg =verifica_local(usuario_id)
        if tem_local:
            return JsonResponse({
                'message': msg,
                'redirect_url': '/home'
            })

        return render(request, 'Projeto/cadastro_local.html')

def verifica_local(usuario_id):
    try:
        barbeiro = Barbeiro.objects.get(id=usuario_id)
        if Local.objects.filter(barbeirousuarioid=barbeiro).exists():
            return JsonResponse ({"status":True, "msg":"Você já possui um local cadastrado."})
        return False, ""
    except Barbeiro.DoesNotExist:
        return JsonResponse ({"status":False, "msg":"Usuário (barbeiro) não encontrado."})

def cadastrar_local(data):
    nome_local = data.get('nomeLocal')
    rua = data.get('rua', '').strip()
    bairro = data.get('bairro', '').strip()
    numero = data.get('numero', '').strip()
    cidade = data.get('cidadeLocal', '').strip()
    endereco = f"{rua},{bairro},{numero},{cidade}"
    cnpj = data.get('cnpj')
    telefone = data.get('telefone')
    
    try:
        barbeiro = Barbeiro.objects.get(id=data.get('usuario_id'))  # Assumindo que 'usuario_id' é o ID do Barbeiro
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

def editar_local_view(request): 
    print("Método recebido:", request.method)
    print("Headers:", request.headers)
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']

    if request.method == 'POST' and 'application/json' in request.headers.get('Content-Type', ''):
        print("Recebendo dados:", request.body)
        data = json.loads(request.body)
        data['usuario_id'] = usuario_id

        print("chamando a func")
        resultado = editar_local(data)
        return JsonResponse({'success': resultado['status'] == 'success', 'message': resultado.get('message', '')})

    # Se for GET, busca os dados com a função auxiliar
    resultado = recuperar_dados_local(usuario_id)

    if resultado['status'] == 'success':
        return render(request, 'Projeto/editar_local.html', {
            'usuario': resultado['usuario'],
            'local': resultado['local']
        })
    else:
        return redirect('home')

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
        cidade = data.get('cidadeLocal', '').strip()
        endereco = f"{rua},{bairro},{numero},{cidade}"

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

def apagar_local_view(request):
    print("apagar_local_view")
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']

    if request.method == 'POST':
        data = {'usuario_id': usuario_id}
        print("chamando a função apagar_local")
        resultado = apagar_local(data)

        if resultado['status'] == 'success':
            print("sucesso")
            return redirect('home')
        else:
            return render(request, 'Projeto/apagar_local.html', {'error': resultado['message']})

    return render(request, 'Projeto/apagar_local.html')

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

        return JsonResponse ({'status': 'success'})

    except Local.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Local não encontrado'})

    except Barbeiro.DoesNotExist:
        return JsonResponse ({'status': 'error', 'message': 'Barbeiro não encontrado'})

    except Exception as e:
        return JsonResponse ({'status': 'error', 'message': str(e)})
    
def cadastrar_servico_view(request):
    # Recupera o id do usuário logado
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redireciona caso o usuário não esteja logado

    usuario_id = request.session['usuario_id']
    data = {}
    data['usuario_id'] = usuario_id 

    # Se for POST com conteúdo JSON
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            # Carrega os dados JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)
        
        # Adiciona o usuario_id ao JSON data
        data['usuario_id'] = usuario_id

        # Passa o dicionário data para a função de cadastro
        success, msg = cadastrar_servico(data)

        # Retorna a resposta com sucesso ou erro
        print("Resultado do cadastro:", success, msg)
        return JsonResponse({
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        })

    # Se for GET, renderiza o formulário
    return render(request, 'Projeto/cadastro_servicos.html')

def cadastrar_servico(data):
    try:
        barbeiro = Barbeiro.objects.get(id=data.get('usuario_id'))  # Assumindo que 'usuario_id' é o ID do Barbeiro
        local = Local.objects.get(barbeirousuarioid=barbeiro)
    except Barbeiro.DoesNotExist:
        return JsonResponse ({"status": False, "msg": "Usuário (barbeiro) não encontrado"})
    
    # Dados Serviço
    nome_servico_list = data.get('nomeServico', [])
    descricao_servico_list = data.get('descricao', [])
    preco_list = data.get('preco', [])
    tempo_list = data.get('duracao', [])

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

    return JsonResponse ({"status": True, "msg": "Cadastro realizado com sucesso!"})

def cadastrar_horario_view(request):
    # Recupera o id do usuário logado
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redireciona caso o usuário não esteja logado

    usuario_id = request.session['usuario_id']
    data = {}
    data['usuario_id'] = usuario_id 

    # Se for POST com conteúdo JSON
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            # Carrega os dados JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)
        
        # Adiciona o usuario_id ao JSON data
        data['usuario_id'] = usuario_id

        # Passa o dicionário data para a função de cadastro
        success, msg = cadastrar_horario(data)

        # Retorna a resposta com sucesso ou erro
        print("Resultado do cadastro:", success, msg)
        return JsonResponse({
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        })

    # Se for GET, renderiza o formulário
    return render(request, 'Projeto/cadastro_horarios.html')

def cadastrar_horario(data):
    try:
        barbeiro = Barbeiro.objects.get(id=data.get('usuario_id'))  # Assumindo que 'usuario_id' é o ID do Barbeiro
        local = Local.objects.get(barbeirousuarioid=barbeiro)
    except Barbeiro.DoesNotExist:
        return JsonResponse ({"status": False, "msg": "Usuário (barbeiro) não encontrado"})
    
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
                return JsonResponse ({"status": False, "msg": f"Horário inválido: {horario}. Use o formato HH:MM."})

            horario_obj = Horarios(
                dia_semana=dia,
                horarios=horario_formatado,
                idlocal=local
            )
            horario_obj.save()

    return JsonResponse ({"status": True, "msg": "Cadastro realizado com sucesso!"})

def logout_view(request):
    request.session.flush()  # Limpa todos os dados da sessão
    return redirect('login')  # Redireciona para a página de login
