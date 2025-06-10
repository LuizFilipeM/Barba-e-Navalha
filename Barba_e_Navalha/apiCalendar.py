# Barba_e_Navalha/apiCalendar.py

# redesenhar para gerenciar multiplos tokens do calendar, pois várias pessoas vão utilizar.
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import Barbeiro, GoogleApiToken

# Escopo necessário para criar e DELETAR eventos
SCOPES = ["https://www.googleapis.com/auth/calendar"] # Modificado para incluir permissão geral do calendário

# Caminho absoluto para os arquivos de credenciais
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'Barba_e_Navalha', 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'Barba_e_Navalha', 'token.json')


def _get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds

# MODIFICAÇÃO NECESSÁRIA ESTÁ AQUI:
def criar_evento(servico_nome, cliente_nome, barbeiro_nome, data_str, hora_str, duracao_minutos, local_endereco, local_nome):
    try:
        creds = _get_credentials() # Ou sua lógica de credenciais por barbeiro
        service = build("calendar", "v3", credentials=creds)

        start_datetime = datetime.datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M")
        effective_duration = duracao_minutos if duracao_minutos and duracao_minutos > 0 else 30 
        end_datetime = start_datetime + datetime.timedelta(minutes=effective_duration)

        # MODIFICAÇÃO 2: Adicionar 'location' e detalhes do local na 'description'
        evento_body = {
            "summary": f"{servico_nome} para {cliente_nome} com {barbeiro_nome}",
            "location": local_endereco, # <<< CAMPO PRINCIPAL PARA O MAPA
            "description": (
                f"<b>Cliente:</b> {cliente_nome}\n"
                f"<b>Serviço:</b> {servico_nome}\n"
                f"<b>Barbeiro:</b> {barbeiro_nome}\n"
                f"<b>Duração:</b> {effective_duration} min\n\n"
                f"<b>Local:</b> {local_nome}\n"
                f"<b>Endereço:</b> {local_endereco}"
            ),
            "start": {"dateTime": start_datetime.isoformat(), "timeZone": "America/Sao_Paulo"},
            "end": {"dateTime": end_datetime.isoformat(), "timeZone": "America/Sao_Paulo"},
        }
        event = service.events().insert(calendarId="primary", body=evento_body).execute()
        return True, event.get('id'), event.get('htmlLink')
    except Exception as e:
        # ... (seu tratamento de erro) ...
        return False, None, str(e)

def deletar_evento_calendar(event_id):
    """Deleta um evento do Google Calendar usando o event_id."""
    try:
        creds = _get_credentials()
        service = build("calendar", "v3", credentials=creds)

        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"✅ Evento {event_id} deletado do Google Calendar.")
        return True, "Evento deletado com sucesso do Google Calendar."

    except HttpError as error:
        if error.resp.status == 404: # Evento não encontrado
            print(f"⚠️ Evento {event_id} não encontrado no Google Calendar. Pode já ter sido deletado.")
            return True, "Evento não encontrado no Google Calendar (possivelmente já deletado)."
        print(f"❌ Erro na API do Google Calendar ao deletar evento {event_id}: {error}")
        return False, f"Erro do Google Calendar ao deletar evento: {error}"
    except Exception as e:
        print(f"❌ Erro interno ao deletar evento {event_id}: {e}")
        return False, str(e)

def atualizar_evento_calendar(event_id, novo_servico_nome, nome_cliente, nome_barbeiro, nova_data_str, nova_hora_str, duracao_minutos, local_endereco, local_nome):
    try:
        creds = _get_credentials()
        service = build("calendar", "v3", credentials=creds)

        start_datetime = datetime.datetime.strptime(f"{nova_data_str} {nova_hora_str}", "%Y-%m-%d %H:%M")
        effective_duration = duracao_minutos if duracao_minutos and duracao_minutos > 0 else 30
        end_datetime = start_datetime + datetime.timedelta(minutes=effective_duration)

        updated_event_body = {
            "summary": f"{novo_servico_nome} para {nome_cliente} com {nome_barbeiro}",
            "location": local_endereco, # <<< CAMPO PRINCIPAL PARA O MAPA
            "description": (
                f"<b>Cliente:</b> {nome_cliente}\n"
                f"<b>Serviço:</b> {novo_servico_nome}\n"
                f"<b>Barbeiro:</b> {nome_barbeiro}\n"
                f"<b>Duração:</b> {effective_duration} min\n\n"
                f"<b>Local:</b> {local_nome}\n"
                f"<b>Endereço:</b> {local_endereco}"
            ),
            "start": {"dateTime": start_datetime.isoformat(), "timeZone": "America/Sao_Paulo"},
            "end": {"dateTime": end_datetime.isoformat(), "timeZone": "America/Sao_Paulo"},
        }

        event = service.events().update(calendarId="primary", eventId=event_id, body=updated_event_body).execute()
        return True, f"Evento {event_id} atualizado com sucesso no Google Calendar."
    except Exception as e:
        print(f"❌ Erro interno ao atualizar evento {event_id}: {e}")
        return False, str(e)
    
def listar_eventos_calendar(time_min=None):
    """
    Lista eventos de um calendário a partir de uma data/hora mínima.

    Args:
        time_min (str, optional): A data/hora mínima (formato ISO 8601) para filtrar eventos.
                                  Se None, busca eventos futuros a partir de agora.

    Returns:
        tuple: Uma tupla contendo (sucesso, lista_de_eventos_ou_mensagem_de_erro).
               Em caso de sucesso, o segundo elemento é uma lista de dicionários de eventos.
               Em caso de falha, é uma string com a mensagem de erro.
    """
    try:
        creds = _get_credentials()
        service = build("calendar", "v3", credentials=creds)

        if time_min is None:
            # Pega o horário atual no formato UTC, que é o esperado pela API
            time_min = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indica UTC

        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        eventos = events_result.get('items', [])
        return True, eventos

    except HttpError as error:
        print(f"❌ Erro na API do Google Calendar ao listar eventos: {error}")
        return False, f"Erro do Google Calendar ao listar eventos: {error}"
    except Exception as e:
        print(f"❌ Erro interno ao listar eventos: {e}")
        return False, str(e)