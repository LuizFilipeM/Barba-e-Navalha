# Projeto/controlador.py
from django.shortcuts import render
from ..Login_Autenticacao.views import login, cadastro, editar_perfil, deletar_perfil
from ..Gestao_Agendamento.views import inserir_agendamento, remover_agendamento, atualiza_agendamento, lista_agendamentos
import json
from django.http import JsonResponse


def processar_requisicao(request):
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        url = request.path
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Json inválido'}, status=400)

        acao = data.get('acao')
        dados = data.get('dados')

        if not acao or not dados:
            return JsonResponse({'success': False, 'message': 'Ação ou dados não fornecidos'}, status=400)

        # Login e Cadastro
        if url == '/login/':
            success, msg, user_id, tipo, nome = login(dados)

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

        elif url == '/cadastro/':
            success, msg,  = cadastro(dados)

            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/login' if success else ''
            })

        elif url == '/editar_perfil/':
            success, msg = editar_perfil(dados)
            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/home' if success else ''
            })

        elif url == '/deletar_perfil/':
            success, msg = deletar_perfil(dados)
            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/home' if success else ''
            })


        # Agendamento
        elif url == '/agendar/':
            success, msg = inserir_agendamento(dados)
            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/home' if success else ''
            })

        elif url == '/atualizar_agendamento/':
            success, msg = atualiza_agendamento(dados)
            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/home' if success else ''
            })

        elif url == '/listar_agendamentos/':
            success, msg = lista_agendamentos(dados)
            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/home' if success else ''
            })

        elif url == '/remover_agendamento/':
            success, msg = remover_agendamento(dados)
            return JsonResponse({
                'success': success,
                'message': msg,
                'redirect_url': '/home' if success else ''
            })

    # Caso seja GET, apenas renderiza o formulário normalmente
    return render(request, 'Projeto/login.html')