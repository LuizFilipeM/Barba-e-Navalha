# ESTA FALTANDO RECEBER O JSON DO CONTROLLER

from django.shortcuts import render, redirect
from django.urls import NoReverseMatch
from .models import Cliente, Barbeiro, Agenda
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# 
def render_template(request):
    return render(request, 'home.html')

def inserir_agendamento(request):
    if request.method == 'POST':
        cliente_nome = request.POST.get('cliente')
        barbeiro_nome = request.POST.get('barbeiro')
        servico_id = request.POST.get('servico')
        data = request.POST.get('data')
        horario = request.POST.get('horario')

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT "ID" FROM "Cliente" WHERE "Nome" = %s', [cliente_nome])
                cliente_id = cursor.fetchone()
                if cliente_id is None:
                    return HttpResponse("O cliente nao existe no banco de dados.")

                cursor.execute('SELECT "ID" FROM "Barbeiro" WHERE "Nome" = %s', [barbeiro_nome])
                barbeiro_id = cursor.fetchone()
                if barbeiro_id is None:
                    return HttpResponse("O barbeiro nao existe no banco de dados.")

                cursor.execute(
                    'SELECT "ID" FROM "Agenda" WHERE "Data" = %s AND "Hora" = %s AND "IDBarbeiro" = %s',
                    [data, horario, barbeiro_id[0]])
                existing_agendamento = cursor.fetchone()
                if existing_agendamento:
                    return HttpResponse("Já existe um agendamento para este barbeiro nesta data e horário.")
                
                cursor.execute(
                    'INSERT INTO "Agenda" ("Data", "Hora", "IDBarbeiro", "IDCliente", "IDServicos") VALUES (%s, %s, %s, %s, %s) RETURNING "ID"',
                    [data, horario, barbeiro_id[0], cliente_id[0], servico_id])
                agenda_id = cursor.fetchone()[0]
                connection.commit()
                return HttpResponse("Agendamento adicionado com sucesso!")

        except Exception as e:
            connection.rollback()
            return HttpResponse(f"Erro ao inserir agendamento: {e}")

    return render(request, 'inserir_agendamento.html')

def remover_agendamento(request):
    if request.method == 'POST' and 'cliente_id' in request.POST:
        cliente_id = request.POST.get('cliente_id')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
            return render(request, 'remover_agendamento.html')

        agendamentos = Agenda.objects.filter(idcliente=cliente)

        if not agendamentos:
            messages.error(request, 'Nenhum agendamento encontrado para este cliente.')
            return render(request, 'remover_agendamento.html')

        return render(request, 'remover_agendamento.html', {'agendamentos': agendamentos})

    if request.method == 'POST' and 'agendamento_id' in request.POST:
        agendamento_id = request.POST.get('agendamento_id')

        try:
            agendamento = Agenda.objects.get(id=agendamento_id)
        except Agenda.DoesNotExist:
            messages.error(request, 'Agendamento não encontrado.')
            return render(request, 'remover_agendamento.html')

        agendamento.delete()
        messages.success(request, 'Agendamento removido com sucesso.')
        return render(request, 'remover_agendamento.html')

    return render(request, 'remover_agendamento.html')

@csrf_exempt
def atualiza_agendamento(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')

        if 'agendamento_id' in request.POST:
            agendamento_id = request.POST.get('agendamento_id')
            nova_data = request.POST.get('data')
            novo_horario = request.POST.get('hora')
            novo_servico = request.POST.get('servico')

            try:
                agendamento = Agenda.objects.get(id=agendamento_id, idcliente=cliente_id)
                if nova_data:
                    agendamento.data = nova_data
                if novo_horario:
                    agendamento.hora = novo_horario
                if novo_servico:
                    agendamento.idservicos_id = novo_servico
                agendamento.save()
                messages.success(request, 'Agendamento atualizado com sucesso!')
            except Agenda.DoesNotExist:
                messages.error(request, 'Agendamento não encontrado.')
            return redirect('atualizar_agendamento')

        if cliente_id:
            agendamentos = Agenda.objects.filter(idcliente=cliente_id)
            return render(request, 'atualizar_agendamento.html', {'agendamentos': agendamentos, 'cliente_id': cliente_id})
    
    return render(request, 'atualizar_agendamento.html')
def lista_agendamentos(request):
    cliente_nome = request.GET.get('cliente')
    agendamentos = []

    if cliente_nome:
        try:
            cliente = Cliente.objects.get(nome=cliente_nome)
            agendamentos = Agenda.objects.filter(idcliente=cliente)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')

    return render(request, 'lista_agendamentos.html', {'agendamentos': agendamentos})
