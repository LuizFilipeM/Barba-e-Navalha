import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .controller import processar_requisicao  # Controller decide a lógica
from .login_cadastro import login  # usado no login_view
from django.contrib import messages
from .gestao_agendamento import listar_locais_barbeiro_logica
from .models import Barbeiro

def teste_controller_view(request):
    return render(request, 'teste_controller.html')


@csrf_exempt
def central_view(request):
    if request.method in ['POST', 'GET']:
        try:
            resposta = processar_requisicao(request)
            return JsonResponse(resposta)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Método não permitido"}, status=405)

@csrf_exempt
def mostrar_locais_do_barbeiro(request, barbeiro_id):
    """
    Esta view é dedicada a renderizar a página HTML que mostra
    os locais de um barbeiro específico.
    """
    try:
        # Prepara os dados para a função lógica, assim como o controller faria
        dados_para_logica = {'barbeiro_id': barbeiro_id}
        
        # Chama a mesma função lógica que você já tem
        success, resultado = listar_locais_barbeiro_logica(dados_para_logica)
        
        contexto = {
            'success': success,
            'dados': resultado,  # Passa o resultado (que contém nome e lista de locais)
            'barbeiro_id': barbeiro_id # Passa o ID para o template se necessário
        }
        
        # Renderiza o template HTML com os dados
        return render(request, 'barbearia/locais_do_barbeiro.html', contexto)

    except Exception as e:
        # Em caso de erro, você pode renderizar uma página de erro ou levantar um Http404
        print(f"Erro ao buscar locais do barbeiro: {e}")
        raise Http404("Página não encontrada ou erro ao processar a requisição.")
# <<< FIM DA ALTERAÇÃO >>>