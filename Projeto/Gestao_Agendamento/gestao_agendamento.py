# BACK-END GESTAO AGENDAMENTO

# Barba_e_Navalha/gestao_agendamento.py
from django.http import JsonResponse
from Projeto.Login_Autenticacao.models import Barbeiro, Cliente, Local, Servicos, Agenda
from .models import *
from .apiCalendar import criar_evento, deletar_evento_calendar, atualizar_evento_calendar, listar_eventos_calendar
from .apiMaps import gerar_url_mapa_incorporado
from django.db.models import Q
import datetime

def _check_overlap(start1, end1, start2, end2):
    """Verifica se dois intervalos de tempo [start1, end1) e [start2, end2) se sobrepõem."""
    return start1 < end2 and end1 > start2

def inserir_agendamento_logica(data):
    try:
        # --- Obtenção de dados da requisição ---
        cliente_nome_str = data.get('cliente')
        barbeiro_solicitado_nome_str = data.get('barbeiro')
        servico_id_str = data.get('servico')
        data_agendamento_str = data.get('data')
        horario_str = data.get('horario')

        if not all([cliente_nome_str, barbeiro_solicitado_nome_str, servico_id_str, data_agendamento_str, horario_str]):
            print(cliente_nome_str, barbeiro_solicitado_nome_str, servico_id_str, data_agendamento_str, horario_str)
            return JsonResponse({'status':False, 'msg':"Dados incompletos para o agendamento."})

        # --- Buscando objetos no banco ---
        cliente = Cliente.objects.filter(nome=cliente_nome_str).first()
        if not cliente:
            return JsonResponse({'status':False, 'msg': "Cliente não encontrado."})
            
        barbeiro_solicitado = Barbeiro.objects.filter(nome=barbeiro_solicitado_nome_str).first()
        if not barbeiro_solicitado:
            return JsonResponse({'status':False, 'msg': f"Barbeiro '{barbeiro_solicitado_nome_str}' não encontrado."})

        local_do_barbeiro = Local.objects.filter(barbeirousuarioid=barbeiro_solicitado).first()
        if not local_do_barbeiro:
            return JsonResponse({'status':False, 'msg': f"O barbeiro {barbeiro_solicitado.nome} não está associado a nenhum local de trabalho."})

        try:
            servico_id = int(servico_id_str)
            novo_servico = Servicos.objects.get(id=servico_id, idlocal=local_do_barbeiro)
            if novo_servico.tempo is None or novo_servico.tempo <= 0:
                return JsonResponse({'status':False, 'msg': f"O serviço '{novo_servico.nome}' não possui uma duração válida cadastrada."})
            duracao_novo_servico_min = novo_servico.tempo
        except Servicos.DoesNotExist:
            return JsonResponse({'status':False, 'msg': f"Serviço não encontrado ou não oferecido no local '{local_do_barbeiro.nome_local}'."})
        except (ValueError, TypeError):
            return JsonResponse({'status':False, 'msg': "ID do serviço inválido."})

        # --- Preparação dos horários do NOVO agendamento ---
        try:
            data_obj = datetime.datetime.strptime(data_agendamento_str, "%Y-%m-%d").date()
            hora_obj = datetime.datetime.strptime(horario_str, "%H:%M").time()
        except ValueError:
            return JsonResponse({'status':False, 'msg': "Formato de data ou hora inválido. Use YYYY-MM-DD e HH:MM."})

        novo_agendamento_inicio_dt = datetime.datetime.combine(data_obj, hora_obj)
        novo_agendamento_fim_dt = novo_agendamento_inicio_dt + datetime.timedelta(minutes=duracao_novo_servico_min)
        print(f"DEBUG: Tentando agendar de {novo_agendamento_inicio_dt} até {novo_agendamento_fim_dt}")

        # --- INÍCIO DA VERIFICAÇÃO DE CONFLITOS CORRIGIDA ---

        # 1. VERIFICAÇÃO DE CONFLITO PARA O BARBEIRO
        agendamentos_barbeiro_no_dia = Agenda.objects.filter(idbarbeiro=barbeiro_solicitado, data=data_obj).select_related('idservicos')
        for ag_existente in agendamentos_barbeiro_no_dia:
            if ag_existente.idservicos and ag_existente.idservicos.tempo:
                existente_inicio_dt = datetime.datetime.combine(ag_existente.data, ag_existente.hora)
                existente_fim_dt = existente_inicio_dt + datetime.timedelta(minutes=ag_existente.idservicos.tempo)
                
                print(f"DEBUG Barbeiro: Verificando conflito com agendamento existente ID {ag_existente.id} das {existente_inicio_dt} às {existente_fim_dt}")
                if _check_overlap(novo_agendamento_inicio_dt, novo_agendamento_fim_dt, existente_inicio_dt, existente_fim_dt):
                    # Lógica de sugestão de outros barbeiros...
                    # ... (esta parte já estava correta, então a omiti para focar na correção do bug)
                    return JsonResponse({'status':False, 'msg': f"O barbeiro {barbeiro_solicitado.nome} já possui um agendamento conflitante neste horário."})

        # 2. VERIFICAÇÃO DE CONFLITO PARA O CLIENTE
        agendamentos_cliente_no_dia = Agenda.objects.filter(idcliente=cliente, data=data_obj).select_related('idservicos')
        print(f"DEBUG Cliente: Encontrados {agendamentos_cliente_no_dia.count()} agendamentos para o cliente {cliente.nome} no dia {data_obj}")
        
        for ag_existente in agendamentos_cliente_no_dia:
            if ag_existente.idservicos and ag_existente.idservicos.tempo:
                existente_inicio_dt = datetime.datetime.combine(ag_existente.data, ag_existente.hora)
                existente_fim_dt = existente_inicio_dt + datetime.timedelta(minutes=ag_existente.idservicos.tempo)
                
                print(f"DEBUG Cliente: Verificando conflito com agendamento existente ID {ag_existente.id} das {existente_inicio_dt} às {existente_fim_dt}")
                if _check_overlap(novo_agendamento_inicio_dt, novo_agendamento_fim_dt, existente_inicio_dt, existente_fim_dt):
                    return JsonResponse({'status':False, 'msg':f"Você (cliente {cliente.nome}) já possui um agendamento conflitante neste horário ({existente_inicio_dt.strftime('%H:%M')} às {existente_fim_dt.strftime('%H:%M')})."})

        # --- FIM DA VERIFICAÇÃO DE CONFLITOS ---

        # Se não houver conflitos, prosseguir com a criação
        success_calendar, event_id_calendar, msg_calendar_or_link = criar_evento(
            novo_servico.nome, cliente.nome, barbeiro_solicitado.nome,
            data_agendamento_str, horario_str, duracao_novo_servico_min,
            local_do_barbeiro.endereco, local_do_barbeiro.nome_local
        )

        if not success_calendar:
            return JsonResponse({'status':False,'msg': f"Falha ao criar evento no Google Calendar: {msg_calendar_or_link}"})

        novo_agendamento_db = Agenda.objects.create(
            data=data_obj, hora=hora_obj, idbarbeiro=barbeiro_solicitado,
            idcliente=cliente, idservicos=novo_servico,
            google_calendar_event_id=event_id_calendar
        )
        return JsonResponse({'status':True, 'msg': "Agendamento criado com sucesso no sistema e no Google Calendar."})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status':False, 'msg': f"Erro inesperado ao inserir agendamento: {str(e)}"})

def remover_agendamento_logica(data):
    try:
        agendamento_id_app = data.get('agendamento_id')
        if not agendamento_id_app:
            return JsonResponse({"status":False, "msg": "ID do agendamento não fornecido."})

        agendamento = Agenda.objects.get(id=agendamento_id_app)
        google_event_id = agendamento.google_calendar_event_id

        # Tenta deletar o evento do Google Calendar primeiro
        if google_event_id:
            success_calendar, msg_calendar = deletar_evento_calendar(google_event_id)
            if not success_calendar:
                # Loga um aviso se a deleção no Calendar falhar, mas continua
                print(f"⚠️ Aviso: Falha ao deletar evento {google_event_id} do Google Calendar: {msg_calendar}")

        # Remove o agendamento do banco de dados local
        agendamento.delete()
        return JsonResponse({"status":True, "msg": "Agendamento removido com sucesso do sistema."})

    except Agenda.DoesNotExist:
        return JsonResponse({"status":False, "msg": "Agendamento não encontrado no sistema."})
    except Exception as e:
        return JsonResponse({"status":False, "msg": str(e)})

def atualiza_agendamento_logica(data):
    try:
        agendamento_id = data.get('agendamento_id')
        if not agendamento_id:
            return JsonResponse({"status":False, "msg": "ID do agendamento não fornecido para atualização."})

        agendamento = Agenda.objects.select_related('idcliente', 'idbarbeiro', 'idservicos').get(id=agendamento_id)
        
        updated_fields_local = False
        if data.get('data'):
            agendamento.data = data['data']
            updated_fields_local = True
        if data.get('hora'):
            agendamento.hora = data['hora']
            updated_fields_local = True
        
        # Se um novo serviço for enviado, valida se ele pertence ao local do barbeiro
        if data.get('servico'):
            local_do_barbeiro = Local.objects.filter(barbeirousuarioid=agendamento.idbarbeiro).first()
            if not local_do_barbeiro:
                 return JsonResponse({"status":False, "msg": "Não foi possível validar o serviço pois o barbeiro não possui um local de trabalho."})
            try:
                novo_servico_id = int(data['servico'])
                if agendamento.idservicos_id != novo_servico_id:
                    # Busca o novo serviço garantindo que ele pertence ao local correto
                    novo_servico_obj = Servicos.objects.get(id=novo_servico_id, idlocal=local_do_barbeiro)
                    agendamento.idservicos = novo_servico_obj
                    updated_fields_local = True
            except Servicos.DoesNotExist:
                return JsonResponse({"status":False, "msg": f"Novo serviço não encontrado ou não oferecido no local '{local_do_barbeiro.nome_local}'."})
            except (ValueError, TypeError):
                return JsonResponse({"status":False, "msg": "ID do novo serviço inválido."})

        # Salva as alterações no banco de dados se houver alguma
        if updated_fields_local:
            agendamento.save()
            msg_local = "Agendamento atualizado com sucesso no sistema."
        else:
            msg_local = "Nenhum dado foi alterado no sistema."
            
        # CORREÇÃO: A lógica de sincronização do calendário agora é executada se houver um evento para sincronizar.
        if agendamento.google_calendar_event_id:
            barbeiro_do_agendamento = agendamento.idbarbeiro
            local_do_barbeiro = Local.objects.filter(barbeirousuarioid=barbeiro_do_agendamento).first()
            
            if not local_do_barbeiro:
                return JsonResponse({"status":True, "msg": f"{msg_local} (Aviso: não foi possível sincronizar o calendário pois o barbeiro não tem um local definido)."})

            # Prepara todos os dados do agendamento (já atualizados) para a API
            nome_servico_atualizado = agendamento.idservicos.nome
            duracao_atualizada = agendamento.idservicos.tempo
            data_str_calendar = agendamento.data.strftime('%Y-%m-%d') if isinstance(agendamento.data, datetime.date) else str(agendamento.data)
            hora_str_calendar = agendamento.hora.strftime('%H:%M') if isinstance(agendamento.hora, datetime.time) else str(agendamento.hora)

            success_calendar, msg_calendar = atualizar_evento_calendar(
                event_id=agendamento.google_calendar_event_id,
                novo_servico_nome=nome_servico_atualizado,
                nome_cliente=agendamento.idcliente.nome,
                nome_barbeiro=barbeiro_do_agendamento.nome,
                nova_data_str=data_str_calendar,
                nova_hora_str=hora_str_calendar,
                duracao_minutos=duracao_atualizada,
                local_endereco=local_do_barbeiro.endereco,
                local_nome=local_do_barbeiro.nome_local
            )
            
            if success_calendar:
                return JsonResponse({"status":True, "msg": f"{msg_local} E o evento no Google Calendar foi sincronizado."})
            else:
                return JsonResponse({"status":True, "msg": f"{msg_local} (Aviso: falha ao sincronizar o evento no Google Calendar: {msg_calendar})."})

        # Se não houve alterações e não há evento no Google Calendar, apenas retorna a mensagem local.
        return JsonResponse({"status":True, "msg": msg_local})

    except Agenda.DoesNotExist:
        return JsonResponse({"status":False, "msg": "Agendamento não encontrado."})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status":False, "msg": f"Erro inesperado ao atualizar agendamento: {str(e)}"})

def lista_agendamentos_logica(data):
    try:
        nome_cliente = data.get('cliente')
        if not nome_cliente:
            return JsonResponse({"status":False, "msg": "Nome do cliente não fornecido"})

        cliente = Cliente.objects.filter(nome=nome_cliente).first()
        if not cliente:
            return JsonResponse({"status":False, "msg": "Cliente não encontrado."})

        # Obter data e hora atuais
        agora = datetime.datetime.now()
        data_atual = agora.date()
        hora_atual = agora.time()

        # Filtro para pegar agendamentos futuros a partir do momento atual
        filtro_futuros = Q(data__gt=data_atual) | Q(data=data_atual, hora__gte=hora_atual)

        # A lógica de sincronização com o Calendar continua a mesma
        success_calendar, eventos_do_calendar = listar_eventos_calendar()
        if not success_calendar:
            return JsonResponse({"status":False, "msg":eventos_do_calendar})
            
        ids_no_calendario = {evento['id'] for evento in eventos_do_calendar}

        # Busca no banco usando o novo filtro de tempo
        agendamentos_do_banco = Agenda.objects.filter(
            filtro_futuros, # Aplica o filtro de tempo
            idcliente=cliente, 
            google_calendar_event_id__in=ids_no_calendario # Filtra apenas os que estão no calendário
        ).select_related('idbarbeiro', 'idservicos').order_by('data', 'hora')

        resultado_final = []
        for agendamento_db in agendamentos_do_banco:
            # O loop agora só processa agendamentos que já foram filtrados
            ag_data = {
                'id': agendamento_db.id,
                'data': agendamento_db.data.strftime('%d/%m/%Y'),
                'hora': agendamento_db.hora.strftime('%H:%M'),
                'barbeiro_nome': agendamento_db.idbarbeiro.nome if agendamento_db.idbarbeiro else 'N/A',
                'servico_nome': agendamento_db.idservicos.nome if agendamento_db.idservicos else 'N/A',
            }
            if agendamento_db.idbarbeiro:
                local_barbeiro = Local.objects.filter(barbeirousuarioid=agendamento_db.idbarbeiro).first()
                if local_barbeiro:
                    ag_data['local_nome'] = local_barbeiro.nome_local
                    ag_data['local_endereco'] = local_barbeiro.endereco
            
            resultado_final.append(ag_data)

        return JsonResponse({"status":True, "data": resultado_final})

    except Exception as e:
        # ... (seu tratamento de erro)
        return JsonResponse({"status":False, "msg": f"Erro inesperado ao listar agendamentos: {str(e)}"})

def obter_local_agendamento_logica(data):
    """
    Encontra o local de trabalho do barbeiro para um agendamento específico
    e retorna os detalhes junto com uma URL do mapa.
    """
    try:
        agendamento_id = data.get('agendamento_id')
        if not agendamento_id:
            return JsonResponse({"status":False, "msg": "ID do agendamento não fornecido."})

        # Busca o agendamento e o barbeiro relacionado
        agendamento = Agenda.objects.select_related('idbarbeiro').get(id=agendamento_id)
        barbeiro = agendamento.idbarbeiro

        if not barbeiro:
            return JsonResponse({"status":False, "msg": "Agendamento não está associado a nenhum barbeiro."})

        # Com base no modelo, um barbeiro pode estar em vários locais.
        # Esta lógica pega o primeiro local encontrado associado ao barbeiro.
        # Para uma lógica mais precisa, a tabela 'Agenda' poderia ter uma ForeignKey para 'Local'.
        local_obj = Local.objects.filter(barbeirousuarioid=barbeiro).first()

        if not local_obj:
            return JsonResponse({"status":False, "msg": f"Nenhum local de trabalho encontrado para o barbeiro '{barbeiro.nome}'."})

        # Monta a query para o mapa com nome e endereço do local
        query_mapa = f"{local_obj.nome_local}, {local_obj.endereco}"
        map_url = gerar_url_mapa_incorporado(query_mapa)

        resultado = {
            "agendamento_id": agendamento.id,
            "barbeiro_nome": barbeiro.nome,
            "local_nome": local_obj.nome_local,
            "endereco": local_obj.endereco,
            "map_url": map_url
        }
        return JsonResponse({"status":True, "data": resultado})

    except Agenda.DoesNotExist:
        return JsonResponse({"status":False, "msg": "Agendamento não encontrado."})
    except Exception as e:
        return JsonResponse({"status":False, "msg": f"Erro inesperado: {str(e)}"})

def obter_proximo_agendamento_e_local_logica(data):
    try:
        cliente_nome = data.get('cliente_nome')
        if not cliente_nome:
            return JsonResponse({"status":False, "msg": "Nome do cliente não fornecido."})

        cliente = Cliente.objects.filter(nome=cliente_nome).first()
        if not cliente:
            return JsonResponse({"status":False, "msg": "Cliente não encontrado."})

        # Obter data e hora atuais
        agora = datetime.datetime.now()
        data_atual = agora.date()
        hora_atual = agora.time()
        
        # Define o limite de busca para 3 dias a partir de hoje
        data_limite = data_atual + datetime.timedelta(days=3)

        # Filtro para pegar agendamentos futuros a partir do momento atual
        filtro_futuros = Q(data__gt=data_atual) | Q(data=data_atual, hora__gte=hora_atual)

        # Busca o primeiro agendamento que satisfaz o filtro de tempo e o limite de 3 dias
        proximo_agendamento = Agenda.objects.filter(
            filtro_futuros,
            idcliente=cliente,
            data__lt=data_limite # Adiciona o limite de até 3 dias
        ).select_related('idbarbeiro', 'idservicos').order_by('data', 'hora').first()

        if not proximo_agendamento:
            return JsonResponse({"status":False, "msg": "Nenhum agendamento encontrado para os próximos 3 dias."})

        # O restante da lógica para obter local e mapa continua igual
        barbeiro = proximo_agendamento.idbarbeiro
        # ... (código existente para encontrar local e gerar map_url)
        # ...

        local_obj = Local.objects.filter(barbeirousuarioid=barbeiro).first()
        if not local_obj:
            return JsonResponse({"status":False, "msg": "Nenhum local de trabalho encontrado para o barbeiro do próximo agendamento."})

        query_mapa = f"{local_obj.nome_local}, {local_obj.endereco}"
        map_url = gerar_url_mapa_incorporado(query_mapa)

        resultado = {
            "proximo_agendamento": {
                "id": proximo_agendamento.id,
                "data": proximo_agendamento.data.strftime('%d/%m/%Y'),
                "hora": proximo_agendamento.hora.strftime('%H:%M'),
                "servico_nome": proximo_agendamento.idservicos.nome,
                "barbeiro_nome": barbeiro.nome
            },
            "local_info": {
                "nome": local_obj.nome_local,
                "endereco": local_obj.endereco,
                "map_url": map_url
            }
        }
        return JsonResponse({"status":True, "data": resultado})

    except Exception as e:
        # ... (seu tratamento de erro)
        return JsonResponse({"status":False, "msg": f"Erro inesperado: {str(e)}"})

def listar_locais_barbeiro_logica():
    """
    Lista TODOS os locais onde um barbeiro atua e gera um mapa para cada um.
    """
    print("DEBUG: Iniciando a listagem de locais do barbeiro...")
    try:
        #barbeiro_nome = 'barbeiro'
        
        #if not barbeiro_nome:
        #    return JsonResponse({"status":False, "msg": "Nome do barbeiro não fornecido."})

        # Usamos .get() que garante que apenas um barbeiro com esse nome seja encontrado.
        # Se houver nomes duplicados, um erro será lançado, o que é um bom controle.
        #barbeiro = Barbeiro.objects.get(nome=barbeiro_nome)
        
        # CORREÇÃO PRINCIPAL AQUI:
        # Usamos .filter() para buscar TODOS os locais associados a este barbeiro.
        locais_do_barbeiro = Local.objects.all()
        #print(f"DEBUG: Encontrados {locais_do_barbeiro.count()} locais para o barbeiro {barbeiro.nome}.")

        if not locais_do_barbeiro.exists():
            return JsonResponse({"status":False, "msg": "Nenhum local de trabalho encontrado."})

        # Itera sobre CADA local encontrado para construir a lista de resultados.
        locais_com_mapa = []
        for local_obj in locais_do_barbeiro:
            query_mapa = f"{local_obj.nome_local}, {local_obj.endereco}"
            map_url = gerar_url_mapa_incorporado(query_mapa)
            locais_com_mapa.append({
                "local_nome": local_obj.nome_local,
                "endereco": local_obj.endereco,
                "map_url": map_url
            })
            
        resultado = {
            #"barbeiro_nome": barbeiro.nome,
            "locais": locais_com_mapa # A lista agora contém todos os locais
        }
        return JsonResponse({"status":True, "data": resultado})

    #except Barbeiro.DoesNotExist:
    #    return JsonResponse({"status":False, "msg": f"Barbeiro com o nome '{barbeiro_nome}' não encontrado."})
    #except Barbeiro.MultipleObjectsReturned:
    #    return JsonResponse({"status":False, "msg": f"Existe mais de um barbeiro com o nome '{barbeiro_nome}'. Use um identificador único."})
    except Exception as e:
        return JsonResponse({"status":False, "msg": f"Erro inesperado: {str(e)}"})

def listar_agendamentos_barbeiro_logica(data):
    """
    Lista todos os agendamentos FUTUROS de um barbeiro específico,
    a partir do momento exato da consulta.
    """
    try:
        barbeiro_id = data.get('barbeiro_id')
        if not barbeiro_id:
            return JsonResponse({"status":False, "msg": "ID do barbeiro não fornecido."})

        barbeiro = Barbeiro.objects.get(id=barbeiro_id)
        
        agora = datetime.datetime.now()
        data_atual = agora.date()
        hora_atual = agora.time()

        filtro_futuros = Q(data__gt=data_atual) | Q(data=data_atual, hora__gte=hora_atual)

        # <<< INÍCIO DA CORREÇÃO >>>
        # O argumento posicional (filtro_futuros) agora vem ANTES do argumento de palavra-chave.
        agendamentos = Agenda.objects.filter(
            filtro_futuros,
            idbarbeiro=barbeiro
        ).select_related(
            'idcliente', 
            'idservicos'
        ).order_by('data', 'hora')
        # <<< FIM DA CORREÇÃO >>>

        resultado = []
        for ag in agendamentos:
            resultado.append({
                'id': ag.id,
                'data': ag.data.strftime('%d/%m/%Y'),
                'hora': ag.hora.strftime('%H:%M'),
                'cliente_nome': ag.idcliente.nome if ag.idcliente else 'N/A',
                'servico_nome': ag.idservicos.nome if ag.idservicos else 'N/A',
                'servico_duracao': ag.idservicos.tempo if ag.idservicos else 'N/A',
            })

        return JsonResponse({"status":True, "data": resultado})

    except Barbeiro.DoesNotExist:
        return JsonResponse({"status":False, "msg": f"Barbeiro com ID '{barbeiro_id}' não encontrado."})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status":False, "msg": f"Erro inesperado: {str(e)}"})