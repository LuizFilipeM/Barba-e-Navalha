# ESTA FALTANDO RECEBER O JSON DO CONTROLLER

import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cliente, Agenda
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def teste_controller(request):
    return render(request, "teste_controller.html")

@csrf_exempt
def inserir_agendamento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente_nome = data.get("cliente")
            barbeiro_nome = data.get("barbeiro")
            servico_id = data.get("servico")
            data_agendamento = data.get("data")
            horario = data.get("horario")

            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT "ID" FROM "Cliente" WHERE "Nome" = %s', [cliente_nome]
                )
                cliente_id = cursor.fetchone()
                if cliente_id is None:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "O cliente nao existe no banco de dados.",
                        }
                    )

                cursor.execute(
                    'SELECT "ID" FROM "Barbeiro" WHERE "Nome" = %s', [barbeiro_nome]
                )
                barbeiro_id = cursor.fetchone()
                if barbeiro_id is None:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "O barbeiro nao existe no banco de dados.",
                        }
                    )

                cursor.execute(
                    'SELECT "ID" FROM "Agenda" WHERE "Data" = %s AND "Hora" = %s AND "IDBarbeiro" = %s',
                    [data_agendamento, horario, barbeiro_id[0]],
                )
                existing_agendamento = cursor.fetchone()
                if existing_agendamento:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Já existe um agendamento para este barbeiro nesta data e horário.",
                        }
                    )

                cursor.execute(
                    'INSERT INTO "Agenda" ("Data", "Hora", "IDBarbeiro", "IDCliente", "IDServicos") VALUES (%s, %s, %s, %s, %s) RETURNING "ID"',
                    [
                        data_agendamento,
                        horario,
                        barbeiro_id[0],
                        cliente_id[0],
                        servico_id,
                    ],
                )
                agenda_id = cursor.fetchone()[0]
                connection.commit()
                return JsonResponse(
                    {"success": True, "message": "Agendamento adicionado com sucesso!"}
                )

        except Exception as e:
            connection.rollback()
            return JsonResponse(
                {"success": False, "message": f"Erro ao inserir agendamento: {e}"}
            )

    return JsonResponse({"success": False, "message": "Método inválido"})

@csrf_exempt
def remover_agendamento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            agendamento_id = data.get("agendamento_id")

            agendamento = Agenda.objects.get(id=agendamento_id)
            agendamento.delete()
            return JsonResponse(
                {"success": True, "message": "Agendamento removido com sucesso."}
            )
        except Agenda.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Agendamento não encontrado."}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Método inválido"})

@csrf_exempt
def atualiza_agendamento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            agendamento_id = data.get("agendamento_id")
            cliente_id = data.get("cliente_id")
            nova_data = data.get("data")
            novo_horario = data.get("hora")
            novo_servico = data.get("servico")

            agendamento = Agenda.objects.get(id=agendamento_id, idcliente=cliente_id)
            if nova_data:
                agendamento.data = nova_data
            if novo_horario:
                agendamento.hora = novo_horario
            if novo_servico:
                agendamento.idservicos_id = novo_servico
            agendamento.save()
            return JsonResponse(
                {"success": True, "message": "Agendamento atualizado com sucesso!"}
            )
        except Agenda.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Agendamento não encontrado."}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Método inválido"})

def lista_agendamentos(request):
    cliente_nome = request.GET.get("cliente")
    agendamentos = []

    if cliente_nome:
        try:
            cliente = Cliente.objects.get(nome=cliente_nome)
            agendamentos = Agenda.objects.filter(idcliente=cliente)
        except Cliente.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Cliente não encontrado."}
            )

    agendamentos_data = [
        {"id": ag.id, "data": ag.data, "hora": ag.hora, "servico": ag.idservicos.nome}
        for ag in agendamentos
    ]
    return JsonResponse({"success": True, "agendamentos": agendamentos_data})
