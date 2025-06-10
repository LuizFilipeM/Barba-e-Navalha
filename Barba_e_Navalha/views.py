import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .controller import processar_requisicao  # Controller decide a lógica
from .login_cadastro import login  # usado no login_view
from django.contrib import messages

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
