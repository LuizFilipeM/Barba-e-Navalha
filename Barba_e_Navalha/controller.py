# Barba_e_Navalha/controller.py
import json
# Remova 'JsonResponse' dos imports se ele não for usado em nenhum outro lugar neste arquivo.
# from django.http import JsonResponse # Provavelmente não necessário aqui
from django.shortcuts import render # Se usado
from .login_cadastro import (
    login, cadastro, editar_perfil, deletar_perfil
)
from .gestao_agendamento import (
    inserir_agendamento_logica,
    remover_agendamento_logica,
    atualiza_agendamento_logica,
    lista_agendamentos_logica,
    obter_local_agendamento_logica,
    obter_proximo_agendamento_e_local_logica,
    listar_locais_barbeiro_logica,
    listar_agendamentos_barbeiro_logica
)

def processar_requisicao(request):
    dados_resposta = {} # Inicializa um dicionário para a resposta
    url = request.path
    acao = None
    dados_payload = None # Renomeado para evitar conflito com a variável 'dados' no escopo superior

    if request.method == 'GET':
        acao = request.GET.get('acao')
        dados_payload = request.GET.dict()
        dados_payload.pop('acao', None) # Remove 'acao' do payload
    elif request.method == 'POST':
        try:
            corpo_requisicao = json.loads(request.body)
            acao = corpo_requisicao.get('acao')
            dados_payload = corpo_requisicao.get('dados')
        except json.JSONDecodeError:
            # Retorna um dicionário para o erro
            return {'success': False, 'message': 'JSON inválido'}
    else:
        return {'success': False, 'message': 'Método não suportado'}

    if not acao:
        return {'success': False, 'message': 'Ação não fornecida'}

    # Login e Cadastro
    if url == '/login/' or acao == 'login':
        success, msg, user_id, tipo, nome = login(dados_payload)
        if success:
            request.session['usuario_id'] = user_id
            request.session['usuario_tipo'] = tipo
            request.session['usuario_nome'] = nome
        # Retorna um dicionário
        dados_resposta = {
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else '' # Ajuste o redirect conforme necessário
        }
        return dados_resposta

    elif url == '/cadastro/' or acao == 'cadastro':
        success, msg = cadastro(dados_payload)
        # Retorna um dicionário
        dados_resposta = {
            'success': success,
            'message': msg,
            'redirect_url': '/login' if success else '' # Ajuste o redirect
        }
        return dados_resposta

    elif url == '/editar_perfil/' or acao == 'editar_perfil':
        result = editar_perfil(dados_payload) # Assumindo que editar_perfil retorna um dict
        # Retorna um dicionário
        dados_resposta = {
            'success': result.get('status') == 'success',
            'message': result.get('message', ''),
            'redirect_url': '/home' if result.get('status') == 'success' else ''
        }
        return dados_resposta

    elif url == '/deletar_perfil/' or acao == 'deletar_perfil':
        result = deletar_perfil(dados_payload) # Assumindo que deletar_perfil retorna um dict
        # Retorna um dicionário
        dados_resposta = {
            'success': result.get('status') == 'success',
            'message': result.get('message', ''),
            'redirect_url': '/home' if result.get('status') == 'success' else ''
        }
        return dados_resposta

    # Agendamento
    elif url == '/agendar/' or acao == 'inserir_agendamento':
        retorno_logica = inserir_agendamento_logica(dados_payload)
        
        success = retorno_logica[0]
        msg = retorno_logica[1]
        
        dados_resposta = {
            'success': success,
            'message': msg
        }
        
        if success:
            dados_resposta['redirect_url'] = '/home' 
        else:
            dados_resposta['redirect_url'] = '' 
            if len(retorno_logica) == 3: # Se há sugestões
                dados_resposta['sugestoes_barbeiros'] = retorno_logica[2]
        
        return dados_resposta # Retorna o dicionário

    elif url == '/atualizar_agendamento/' or acao == 'atualiza_agendamento':
        success, msg = atualiza_agendamento_logica(dados_payload)
        dados_resposta = {
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        }
        return dados_resposta

    elif url == '/remover_agendamento/' or acao == 'remover_agendamento':
        success, msg = remover_agendamento_logica(dados_payload)
        dados_resposta = {
            'success': success,
            'message': msg,
            'redirect_url': '/home' if success else ''
        }
        return dados_resposta

    elif url == '/listar_agendamentos/' or acao == 'listar_agendamentos':
        success, agendamentos_data = lista_agendamentos_logica(dados_payload)
        dados_resposta = {
            'success': success,
            # Garante que 'agendamentos' seja uma lista em caso de sucesso, ou ausente/erro em caso de falha
            'agendamentos': agendamentos_data if success else [], 
            'message': '' if success else (agendamentos_data if isinstance(agendamentos_data, str) else "Erro ao listar agendamentos")
        }
        # Se lista_agendamentos_logica retorna (False, "mensagem de erro")
        if not success:
             dados_resposta['message'] = agendamentos_data

        return dados_resposta
    
    elif url == '/obter_proximo_agendamento/' or acao == 'obter_proximo_agendamento':
        success, resultado = obter_proximo_agendamento_e_local_logica(dados_payload)
        return {
            'success': success,
            'resultado': resultado if success else None,
            'message': '' if success else resultado
        }

    elif url == '/listar_locais_barbeiro/' or acao == 'listar_locais_barbeiro':
        success, resultado = listar_locais_barbeiro_logica(dados_payload)
        return {
            'success': success,
            'resultado': resultado if success else None,
            'message': '' if success else resultado
        }
    elif url == '/listar_agendamentos_barbeiro/' or acao == 'listar_agendamentos_barbeiro':
        success, resultado = listar_agendamentos_barbeiro_logica(dados_payload)
        return {
            'success': success,
            'agendamentos': resultado if success else [],
            'message': '' if success else resultado
        }
    
    else:
        # Retorna um dicionário para ação desconhecida
        return {"success": False, "message": "Ação desconhecida ou URL não mapeada no controller"}
    
    

    # Este return não deveria ser alcançado se a lógica if/elif cobrir todos os casos
    # ou se os blocos if/elif sempre retornarem. Adicionado para garantir que sempre retorne um dict.
    # return {"success": False, "message": "Fluxo inesperado no controller"}