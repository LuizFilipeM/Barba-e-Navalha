# BACK-END GESTAO AGENDAMENTO


from django.http import JsonResponse
from Projeto.Login_Autenticacao.models import *
from .apiCalendar import criar_evento, deletar_evento_calendar, atualizar_evento_calendar, listar_eventos_calendar
from .apiMaps import gerar_url_mapa_incorporado
from django.db.models import Q
import datetime
import traceback

def _check_overlap(start1, end1, start2, end2):
    """Verifica se dois intervalos de tempo [start1, end1) e [start2, end2) se sobrepõem."""
    return start1 < end2 and end1 > start2

def inserir_agendamento_logica(data):
    try:
        # 1. Obtenção e Validação dos Dados de Entrada
        cliente_nome_str = data.get('cliente')
        barbeiro_solicitado_nome_str = data.get('barbeiro')
        servico_id_str = data.get('servico')
        data_agendamento_str = data.get('data')
        horario_str = data.get('horario')

        if not all([cliente_nome_str, barbeiro_solicitado_nome_str, servico_id_str, data_agendamento_str, horario_str]):
            return False, "Dados incompletos para o agendamento."

        # 2. Busca dos Objetos no Banco de Dados
        cliente = Cliente.objects.filter(nome=cliente_nome_str).first()
        if not cliente: return False, f"Cliente '{cliente_nome_str}' não encontrado."
            
        barbeiro_solicitado = Barbeiro.objects.filter(nome=barbeiro_solicitado_nome_str).first()
        if not barbeiro_solicitado: return False, f"Barbeiro '{barbeiro_solicitado_nome_str}' não encontrado."

        local_do_barbeiro = Local.objects.filter(barbeirousuarioid=barbeiro_solicitado).first()
        if not local_do_barbeiro: return False, f"O barbeiro {barbeiro_solicitado.nome} não está associado a nenhum local."

        try:
            novo_servico = Servicos.objects.get(id=int(servico_id_str), idlocal=local_do_barbeiro)
            if novo_servico.tempo is None or novo_servico.tempo <= 0:
                return False, f"O serviço '{novo_servico.nome}' não possui uma duração válida."
            duracao_novo_servico_min = novo_servico.tempo
        except Servicos.DoesNotExist:
            return False, f"Serviço não encontrado ou não oferecido no local '{local_do_barbeiro.nome_local}'."
        except (ValueError, TypeError):
            return False, "ID do serviço inválido."

        # 3. Preparação dos Horários
        try:
            data_obj = datetime.datetime.strptime(data_agendamento_str, "%Y-%m-%d").date()
            hora_obj = datetime.datetime.strptime(horario_str, "%H:%M").time()
        except ValueError:
            return False, "Formato de data ou hora inválido. Use YYYY-MM-DD e HH:MM."

        novo_agendamento_inicio_dt = datetime.datetime.combine(data_obj, hora_obj)
        novo_agendamento_fim_dt = novo_agendamento_inicio_dt + datetime.timedelta(minutes=duracao_novo_servico_min)

        # 4. Verificação de Conflitos
        # Conflito para o Barbeiro
        agendamentos_barbeiro_no_dia = Agenda.objects.filter(idbarbeiro=barbeiro_solicitado, data=data_obj).select_related('idservicos')
        for ag_existente in agendamentos_barbeiro_no_dia:
            if ag_existente.idservicos and ag_existente.idservicos.tempo:
                existente_inicio_dt = datetime.datetime.combine(ag_existente.data, ag_existente.hora)
                existente_fim_dt = existente_inicio_dt + datetime.timedelta(minutes=ag_existente.idservicos.tempo)
                if _check_overlap(novo_agendamento_inicio_dt, novo_agendamento_fim_dt, existente_inicio_dt, existente_fim_dt):
                    # Se houver conflito, retorna a mensagem de erro detalhada e para a execução.
                    return False, f"O barbeiro {barbeiro_solicitado.nome} já possui um agendamento conflitante das {existente_inicio_dt.strftime('%H:%M')} às {existente_fim_dt.strftime('%H:%M')}."

        # Conflito para o Cliente
        agendamentos_cliente_no_dia = Agenda.objects.filter(idcliente=cliente, data=data_obj).select_related('idservicos')
        for ag_existente in agendamentos_cliente_no_dia:
            if ag_existente.idservicos and ag_existente.idservicos.tempo:
                existente_inicio_dt = datetime.datetime.combine(ag_existente.data, ag_existente.hora)
                existente_fim_dt = existente_inicio_dt + datetime.timedelta(minutes=ag_existente.idservicos.tempo)
                if _check_overlap(novo_agendamento_inicio_dt, novo_agendamento_fim_dt, existente_inicio_dt, existente_fim_dt):
                    return False, f"Você (cliente {cliente.nome}) já possui um agendamento conflitante neste horário."

        # 5. Se todas as validações passaram, cria o evento e o agendamento
        success_calendar, event_id_calendar, msg_calendar = criar_evento(
            novo_servico.nome, cliente.nome, barbeiro_solicitado.nome,
            data_agendamento_str, horario_str, duracao_novo_servico_min,
            local_do_barbeiro.endereco, local_do_barbeiro.nome_local
        )

        if not success_calendar:
            return False, f"Falha ao criar evento no Google Calendar: {msg_calendar}"

        Agenda.objects.create(
            data=data_obj, hora=hora_obj, idbarbeiro=barbeiro_solicitado,
            idcliente=cliente, idservicos=novo_servico,
            google_calendar_event_id=event_id_calendar
        )
        return True, "Agendamento criado com sucesso."

    except Exception as e:
        traceback.print_exc()
        return False, f"Erro inesperado ao inserir agendamento: {str(e)}"


def remover_agendamento_logica(data):
    try:
        agendamento_id_app = data.get('agendamento_id')
        if not agendamento_id_app:
            return False, "ID do agendamento não fornecido."

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
        return True, "Agendamento removido com sucesso do sistema."

    except Agenda.DoesNotExist:
        return False, "Agendamento não encontrado no sistema."
    except Exception as e:
        return False, str(e)

def atualiza_agendamento_logica(data):
    try:
        agendamento_id = data.get('agendamento_id')
        if not agendamento_id:
            return False, "ID do agendamento não fornecido."

        agendamento = Agenda.objects.select_related('idcliente', 'idbarbeiro', 'idservicos').get(id=agendamento_id)
        
        updated_fields_local = False
        if data.get('data'):
            agendamento.data = data['data']
            updated_fields_local = True
        if data.get('hora'):
            agendamento.hora = data['hora']
            updated_fields_local = True
        
        if data.get('servico'):
            local_do_barbeiro = Local.objects.filter(barbeirousuarioid=agendamento.idbarbeiro).first()
            if not local_do_barbeiro:
                return False, "Barbeiro do agendamento não possui um local de trabalho."
            try:
                novo_servico_id = int(data['servico'])
                if agendamento.idservicos_id != novo_servico_id:
                    novo_servico_obj = Servicos.objects.get(id=novo_servico_id, idlocal=local_do_barbeiro)
                    agendamento.idservicos = novo_servico_obj
                    updated_fields_local = True
            except Servicos.DoesNotExist:
                return False, f"Novo serviço não encontrado ou não oferecido no local."
            except (ValueError, TypeError):
                return False, "ID do novo serviço inválido."

        if updated_fields_local:
            agendamento.save()
            msg_local = "Agendamento atualizado com sucesso."
        else:
            msg_local = "Nenhum dado foi alterado."
            
        if agendamento.google_calendar_event_id:
            local_do_barbeiro = Local.objects.filter(barbeirousuarioid=agendamento.idbarbeiro).first()
            if not local_do_barbeiro:
                return True, f"{msg_local} (Aviso: calendário não sincronizado, barbeiro sem local)."

            data_str_calendar = agendamento.data.strftime('%Y-%m-%d') if isinstance(agendamento.data, datetime.date) else str(agendamento.data)
            hora_str_calendar = agendamento.hora.strftime('%H:%M') if isinstance(agendamento.hora, datetime.time) else str(agendamento.hora)

            success_calendar, msg_calendar = atualizar_evento_calendar(
                event_id=agendamento.google_calendar_event_id,
                # Os outros parâmetros para atualizar o evento no calendar
                barbeiro_id = agendamento.idbarbeiro.id, # Se você implementou o token por usuário
                novo_servico_nome=agendamento.idservicos.nome,
                nome_cliente=agendamento.idcliente.nome,
                nome_barbeiro=agendamento.idbarbeiro.nome,
                nova_data_str=data_str_calendar,
                nova_hora_str=hora_str_calendar,
                duracao_minutos=agendamento.idservicos.tempo,
                local_endereco=local_do_barbeiro.endereco,
                local_nome=local_do_barbeiro.nome_local
            )
            
            if success_calendar:
                return True, f"{msg_local} Evento no Google Calendar também foi atualizado."
            else:
                return True, f"{msg_local} (Aviso: falha ao atualizar no Google Calendar: {msg_calendar})."
        
        return True, msg_local

    except Agenda.DoesNotExist:
        return False, "Agendamento não encontrado."
    except Exception as e:
        traceback.print_exc()
        return False, f"Erro inesperado: {str(e)}"

def lista_agendamentos_logica(data):
    try:
        nome_cliente = data.get('cliente')
        if not nome_cliente:
            return False, "Nome do cliente não fornecido"

        cliente = Cliente.objects.filter(nome=nome_cliente).first()
        if not cliente:
            return False, "Cliente não encontrado."
        
        # Obter data e hora atuais
        agora = datetime.datetime.now()
        data_atual = agora.date()
        hora_atual = agora.time()

        # Filtro para pegar agendamentos futuros a partir do momento atual
        filtro_futuros = Q(data__gt=data_atual) | Q(data=data_atual, hora__gte=hora_atual)

        # A lógica de sincronização com o Calendar continua a mesma
        success_calendar, eventos_do_calendar = listar_eventos_calendar()
        if not success_calendar:
            return False, eventos_do_calendar
            
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

        return True, resultado_final

    except Exception as e:
        # ... (seu tratamento de erro)
        return False, f"Erro inesperado ao listar agendamentos: {str(e)}"
    
def obter_local_agendamento_logica(data):
    """
    Encontra o local de trabalho do barbeiro para um agendamento específico
    e retorna os detalhes junto com uma URL do mapa.
    """
    try:
        agendamento_id = data.get('agendamento_id')
        if not agendamento_id:
            return False, "ID do agendamento não fornecido."

        # Busca o agendamento e o barbeiro relacionado
        agendamento = Agenda.objects.select_related('idbarbeiro').get(id=agendamento_id)
        barbeiro = agendamento.idbarbeiro

        if not barbeiro:
            return False, "Agendamento não está associado a nenhum barbeiro."

        # Com base no modelo, um barbeiro pode estar em vários locais.
        # Esta lógica pega o primeiro local encontrado associado ao barbeiro.
        # Para uma lógica mais precisa, a tabela 'Agenda' poderia ter uma ForeignKey para 'Local'.
        local_obj = Local.objects.filter(barbeirousuarioid=barbeiro).first()

        if not local_obj:
            return False, f"Nenhum local de trabalho encontrado para o barbeiro '{barbeiro.nome}'."

        # Monta a query para o mapa com nome e endereço do local
        # query_mapa = f"{local_obj.nome_local}, {local_obj.endereco}"
        query_mapa = f"{local_obj.endereco}"
        map_url = gerar_url_mapa_incorporado(query_mapa)

        resultado = {
            "agendamento_id": agendamento.id,
            "barbeiro_nome": barbeiro.nome,
            "local_nome": local_obj.nome_local,
            "endereco": local_obj.endereco,
            "map_url": map_url
        }
        return True, resultado

    except Agenda.DoesNotExist:
        return False, "Agendamento não encontrado."
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

def obter_proximo_agendamento_e_local_logica(data):
    try:
        cliente_nome = data.get('cliente_nome')
        if not cliente_nome:
            return False, "Nome do cliente não fornecido."
            
        cliente = Cliente.objects.filter(nome=cliente_nome).first()
        if not cliente:
            return False, "Cliente não encontrado."

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
            return False, "Nenhum agendamento encontrado para os próximos 3 dias."

        # O restante da lógica para obter local e mapa continua igual
        barbeiro = proximo_agendamento.idbarbeiro
       

        local_obj = Local.objects.filter(barbeirousuarioid=barbeiro).first()
        if not local_obj:
            return False, "Nenhum local de trabalho encontrado para o barbeiro do próximo agendamento."

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
        return True, resultado

    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

def listar_locais_barbeiro_logica(data):
    """
    Lista TODOS os locais onde um barbeiro atua e gera um mapa para cada um.
    """
    try:
        barbeiro_nome = data.get('barbeiro_nome')
        if not barbeiro_nome:
            return False, "Nome do barbeiro não fornecido."
        
        # Usamos .get() que garante que apenas um barbeiro com esse nome seja encontrado.
        # Se houver nomes duplicados, um erro será lançado, o que é um bom controle.
        barbeiro = Barbeiro.objects.get(nome=barbeiro_nome)
        
        # CORREÇÃO PRINCIPAL AQUI:
        # Usamos .filter() para buscar TODOS os locais associados a este barbeiro.
        locais_do_barbeiro = Local.objects.filter(barbeirousuarioid=barbeiro)

        if not locais_do_barbeiro.exists():
            return False, f"Nenhum local de trabalho encontrado para o barbeiro {barbeiro.nome}."

        # Itera sobre CADA local encontrado para construir a lista de resultados.
        locais_com_mapa = []
        for local_obj in locais_do_barbeiro:
            # query_mapa = f"{local_obj.nome_local}, {local_obj.endereco}" # Tem que ser nome e local real
            query_mapa = f"{local_obj.endereco}"
            map_url = gerar_url_mapa_incorporado(query_mapa)
            locais_com_mapa.append({
                "local_nome": local_obj.nome_local,
                "endereco": local_obj.endereco,
                "map_url": map_url
            })
            
        resultado = {
            "barbeiro_nome": barbeiro.nome,
            "locais": locais_com_mapa # A lista agora contém todos os locais
        }
        return True, resultado

    except Barbeiro.DoesNotExist:
        return False, f"Barbeiro com o nome '{barbeiro_nome}' não encontrado."
    except Barbeiro.MultipleObjectsReturned:
        return False, f"Existe mais de um barbeiro com o nome '{barbeiro_nome}'. Use um identificador único."
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"
    
def listar_agendamentos_barbeiro_logica(data):
    """
    Lista todos os agendamentos FUTUROS de um barbeiro específico,
    a partir do momento exato da consulta.
    """
    try:
        barbeiro_id = data.get('barbeiro_id')
        if not barbeiro_id:
            return False, "ID do barbeiro não fornecido."
            
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

        return JsonResponse({"status": True, "data": resultado})

    except Barbeiro.DoesNotExist:
        return JsonResponse({"status": False, "msg": f"Barbeiro com ID '{barbeiro_id}' não encontrado."})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": False, "msg": f"Erro inesperado: {str(e)}"})
    
def listar_todas_barbearias_logica():
    """
    Busca e lista todas as barbearias (Locais) cadastradas no banco de dados.
    
    """
    try:
        # Usa .all() para buscar todos os objetos do modelo Local
        todas_as_barbearias = Local.objects.all().order_by('nome_local')
        if not todas_as_barbearias.exists():
            return True, [] # Retorna sucesso com uma lista vazia se não houver barbearias

        resultado = []
        for local in todas_as_barbearias:
            resultado.append({
                'id': local.id,
                'nome_local': local.nome_local,
                'endereco': local.endereco,
                'telefone': local.telefone,
                'cnpj': local.cnpj # Adicionado CNPJ se for útil
            })
        return JsonResponse({"status": True, "data": resultado})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": False, "message": f"Erro inesperado ao listar as barbearias: {str(e)}"})

def listar_todos_servicos_logica():
    """
    Busca e lista todos os serviços cadastrados, incluindo a qual local pertencem.
    """
    try:
        # Usamos .select_related('idlocal') para otimizar a busca, trazendo
        # os dados do Local relacionado na mesma consulta.
        todos_os_servicos = Servicos.objects.select_related('idlocal').all().order_by('nome')
        
        if not todos_os_servicos.exists():
            return True, []

        resultado = []
        for servico in todos_os_servicos:
            resultado.append({
                'id': servico.id,
                'nome': servico.nome,
                'descricao': servico.descricao,
                'preco': f"{servico.preco:.2f}" if servico.preco is not None else "N/A",
                'duracao': servico.tempo,
                'local_id': servico.idlocal.id if servico.idlocal else None,
                'local_nome': servico.idlocal.nome_local if servico.idlocal else "Sem local associado"
            })

        return JsonResponse({"status": True, "data": resultado})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": False, "msg": f"Erro inesperado ao listar os serviços: {str(e)}"})
    
def listar_todos_horarios_logica():
    """
    Busca e lista todos os horários de funcionamento cadastrados,
    indicando a qual Local cada horário pertence.
    """
    try:
        # Usamos .select_related('idlocal') para otimizar a busca,
        # trazendo os dados do Local na mesma consulta ao banco.
        # Ordenamos por nome do local e depois pelo dia da semana.
        todos_os_horarios = Horarios.objects.select_related('idlocal').all().order_by('idlocal__nome_local', 'dia_semana')
        
        if not todos_os_horarios.exists():
            return JsonResponse({"status": True, "data": []}) # Retorna sucesso com uma lista vazia se não houver horários

        resultado = []
        for horario in todos_os_horarios:
            resultado.append({
                'id_horario': horario.id,
                'dia_semana': horario.dia_semana,
                'hora_inicio': horario.hora_inicio.strftime('%H:%M') if horario.hora_inicio else 'N/A',
                'hora_fim': horario.hora_fim.strftime('%H:%M') if horario.hora_fim else 'N/A',
                'local_nome': horario.idlocal.nome_local if horario.idlocal else "Sem local associado"
            })

        return JsonResponse({"status": True, "data": resultado})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": False, "msg": f"Erro inesperado ao listar os horários: {str(e)}"})

def criar_intervalo_logica(data):
    """
    Cria um agendamento especial para o barbeiro que funciona como um intervalo.
    """
    try:
        barbeiro_id = data.get('barbeiro_id')
        data_intervalo_str = data.get('data')
        horario_inicio_str = data.get('horario')
        duracao_minutos = data.get('duracao_minutos')

        if not all([barbeiro_id, data_intervalo_str, horario_inicio_str, duracao_minutos]):
            return JsonResponse({"status": False, "msg": "Dados incompletos para criar o intervalo."})

        barbeiro = Barbeiro.objects.get(id=barbeiro_id)
        
        # Vamos usar um serviço "dummy" chamado "Intervalo" para registrar o bloqueio.
        # Certifique-se de que este serviço existe no seu banco de dados.
        servico_intervalo, created = Servicos.objects.get_or_create(
            nome="Intervalo", 
            defaults={'descricao': 'Bloqueio de tempo', 'preco': 0, 'duracao': 1}
        )

        # A lógica de verificação de conflitos é a mesma da criação de agendamento
        data_obj = datetime.datetime.strptime(data_intervalo_str, "%Y-%m-%d").date()
        hora_obj = datetime.datetime.strptime(horario_inicio_str, "%H:%M").time()
        intervalo_inicio_dt = datetime.datetime.combine(data_obj, hora_obj)
        intervalo_fim_dt = intervalo_inicio_dt + datetime.timedelta(minutes=int(duracao_minutos))

        agendamentos_existentes = Agenda.objects.filter(idbarbeiro=barbeiro, data=data_obj)
        for ag_existente in agendamentos_existentes:
            if ag_existente.idservicos and ag_existente.idservicos.tempo:
                existente_inicio_dt = datetime.datetime.combine(ag_existente.data, ag_existente.hora)
                existente_fim_dt = existente_inicio_dt + datetime.timedelta(minutes=ag_existente.idservicos.tempo)
                if _check_overlap(intervalo_inicio_dt, intervalo_fim_dt, existente_inicio_dt, existente_fim_dt):
                    return JsonResponse({"status": False, "msg": "Você já possui um agendamento de cliente neste horário."})

        # Cria o "agendamento" de intervalo, sem cliente associado (idcliente=None)
        # e com o serviço de intervalo.
        # A duração do serviço será usada para fins de checagem de conflito.
        servico_intervalo.tempo = duracao_minutos
        servico_intervalo.save()

        novo_intervalo = Agenda.objects.create(
            data=data_obj,
            hora=hora_obj,
            idbarbeiro=barbeiro,
            idcliente=None, # Sem cliente
            idservicos=servico_intervalo
        )

        return JsonResponse({"status": True, "msg": f"Intervalo das {horario_inicio_str} às {intervalo_fim_dt.strftime('%H:%M')} criado com sucesso."})

    except Barbeiro.DoesNotExist:
        return JsonResponse({"status": False, "msg": "Barbeiro não encontrado."})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": False, "msg": f"Erro inesperado ao criar intervalo: {str(e)}"})


def editar_servico_barbeiro_logica(data):
    """
    Permite que um barbeiro edite os detalhes de um local de trabalho
    que está associado a ele.
    """
    try:
        barbeiro_id = data.get('barbeiro_id')
        local_id = data.get('local_id')

        if not barbeiro_id or not local_id:
            return JsonResponse({"status": False, "msg": "ID do barbeiro e do local são obrigatórios."})

        # 1. Busca o local que se deseja editar
        local_a_editar = Local.objects.get(id=local_id)

        # 2. VALIDAÇÃO DE SEGURANÇA: Verifica se o local pertence ao barbeiro que fez a requisição
        #    O campo 'barbeirousuarioid' no modelo Local é uma ForeignKey para Barbeiro.
        #    O Django armazena o ID do objeto relacionado em um campo com sufixo '_id'.
        if local_a_editar.barbeirousuarioid_id != int(barbeiro_id):
            return JsonResponse({"status": False, "msg": "Permissão negada. Você só pode editar seus próprios locais de trabalho."})

        # 3. Atualiza os campos se eles foram fornecidos na requisição
        updated = False
        if 'nome_local' in data:
            local_a_editar.nome_local = data['nome_local']
            updated = True
        if 'endereco' in data:
            local_a_editar.endereco = data['endereco']
            updated = True
        if 'telefone' in data:
            local_a_editar.telefone = data['telefone']
            updated = True
        
        if updated:
            local_a_editar.save()
            return JsonResponse({"status":True, "msg": f"Local '{local_a_editar.nome_local}' atualizado com sucesso."})
        else:
            return JsonResponse({"status":False, "msg": "Nenhum dado novo foi fornecido para atualização."}) 

    except Local.DoesNotExist:
        return JsonResponse({"status": False, "msg": "Local com o ID fornecido não foi encontrado."})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": False, "msg": f"Erro inesperado ao editar o local: {str(e)}"})



##############################################################################################################
#                                                                                                            #
# ---------------------------------------- ADICIONAR AO CONTROLLER ------------------------------------------#
#                                                                                                            #
##############################################################################################################



def excluir_servico_barbeiro_logica(data):
    """
    Permite que um barbeiro exclua um serviço, desde que não haja
    agendamentos futuros para ele.
    """
    try:
        barbeiro_id = data.get('barbeiro_id')
        servico_id = data.get('servico_id')

        if not barbeiro_id or not servico_id:
            return False, "ID do barbeiro e do serviço são obrigatórios."

        servico_a_excluir = Servicos.objects.select_related('idlocal__barbeirousuarioid').get(id=servico_id)

        # VALIDAÇÃO DE SEGURANÇA: Mesma validação da função de editar
        if servico_a_excluir.idlocal.barbeirousuarioid_id != int(barbeiro_id):
            return False, "Permissão negada. Você não pode excluir um serviço que não pertence a um de seus locais."

        # VALIDAÇÃO DE INTEGRIDADE: Verifica se o serviço está em uso em agendamentos futuros
        agendamentos_futuros = Agenda.objects.filter(
            idservicos=servico_a_excluir,
            data__gte=datetime.date.today()
        ).exists()

        if agendamentos_futuros:
            return False, "Não é possível excluir este serviço, pois ele já está agendado para clientes no futuro. Cancele os agendamentos primeiro."
        
        nome_servico_excluido = servico_a_excluir.nome
        servico_a_excluir.delete()
        
        return True, f"Serviço '{nome_servico_excluido}' excluído com sucesso."

    except Servicos.DoesNotExist:
        return False, "Serviço com o ID fornecido não foi encontrado."
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Erro inesperado ao excluir o serviço: {str(e)}"
    

##################  FUNÇÃO SIMILAR À editar_local (LOGIN_AUTENTICACAO) ##################

def editar_local_barbeiro_logica(data):
    """
    Permite que um barbeiro edite os detalhes de um serviço oferecido
    em um de seus locais de trabalho.
    """
    try:
        barbeiro_id = data.get('barbeiro_id')
        servico_id = data.get('servico_id')

        if not barbeiro_id or not servico_id:
            return False, "ID do barbeiro e do serviço são obrigatórios."

        # Busca o serviço e pré-carrega o local e o barbeiro associado para a validação
        servico_a_editar = Servicos.objects.select_related('idlocal__barbeirousuarioid').get(id=servico_id)

        # VALIDAÇÃO DE SEGURANÇA: Garante que o serviço pertence a um local deste barbeiro
        if servico_a_editar.idlocal.barbeirousuarioid_id != int(barbeiro_id):
            return False, "Permissão negada. Você não pode editar um serviço que não pertence a um de seus locais."

        # Atualiza os campos que foram enviados na requisição
        updated = False
        if 'nome' in data:
            servico_a_editar.nome = data['nome']
            updated = True
        if 'descricao' in data:
            servico_a_editar.descricao = data['descricao']
            updated = True
        if 'preco' in data:
            servico_a_editar.preco = data['preco']
            updated = True
        if 'duracao' in data:
            servico_a_editar.tempo = data['duracao']
            updated = True
        
        if updated:
            servico_a_editar.save()
            return True, f"Serviço '{servico_a_editar.nome}' atualizado com sucesso."
        else:
            return True, "Nenhum dado novo foi fornecido para atualização."

    except Servicos.DoesNotExist:
        return False, "Serviço com o ID fornecido não foi encontrado."
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Erro inesperado ao editar o serviço: {str(e)}"
    