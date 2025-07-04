# Barba_e_Navalha/apiMaps.py

from django.conf import settings
from urllib.parse import quote

def gerar_url_mapa_incorporado(query: str) -> str:
    """
    Gera uma URL para o Google Maps Embed API usando o modo 'place'.
    """
    api_key = settings.MAPS_API_KEY
    # CORREÇÃO DA URL BASE:
    base_url = "http://www.google.com/maps/embed/v1/place"

    encoded_query = quote(query)
    map_url = f"{base_url}?key={api_key}&q={encoded_query}"
    
    return map_url

def gerar_url_mapa_direcoes(origem: str, destino: str) -> str:
    """
    Gera uma URL para o Google Maps Embed API usando o modo 'directions'.
    """
    api_key = settings.MAPS_API_KEY
    # CORREÇÃO DA URL BASE:
    base_url = "http://www.google.com/maps/embed/v1/directions"
    
    encoded_origin = quote(origem)
    encoded_destination = quote(destino)
    map_url = f"{base_url}?key={api_key}&origin={encoded_origin}&destination={encoded_destination}"

    return map_url