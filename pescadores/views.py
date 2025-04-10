from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Uf, Municipio, AreaPesca, ArtePesca
from rest_framework import status
import json

# Estados
@csrf_exempt
def uf_list(request):
    if request.method == 'GET':
        estados = Uf.objects.all()
        estado_dicts = [estado_to_dict(obs) for obs in estados]
        return JsonResponse({"ufs": estado_dicts})

    elif request.method == 'POST':
        params = json.loads(request.body)
        novo_estado = Uf(nome=params.get('nome'), sigla=params.get('sigla'))
        try:
            novo_estado.full_clean()
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        novo_estado.save()
        return JsonResponse({'uf': estado_to_dict(novo_estado)}, status=status.HTTP_201_CREATED)

@csrf_exempt
def uf_detail(request, pk):
    try:
        estado = Uf.objects.get(pk=pk)
    except Uf.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return JsonResponse({'uf': estado_to_dict(estado)})

    elif request.method == 'DELETE':
        estado.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        data = json.loads(request.body)

        estado.nome = data.get('nome')
        estado.sigla = data.get('sigla')

        try:
            estado.full_clean()
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

        estado.save()
        return JsonResponse({'uf': estado_to_dict(estado)})

# Municipios
@csrf_exempt
def municipio_list(request):
    if request.method == 'GET':
        municipios = Municipio.objects.all()
        municipios_list = [municipio_to_dict(mun) for mun in municipios]
        return JsonResponse({'municipios': municipios_list}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        params = json.loads(request.body)
        uf_id = params.get('uf')
        try:
            uf = Uf.objects.get(pk=uf_id)
        except Uf.DoesNotExist:
            return JsonResponse({"erro": "Uf inválida"}, status=status.HTTP_400_BAD_REQUEST)
        
        nova_cidade = Municipio(nome=params.get('nome'), uf=uf)

        try:
            nova_cidade.full_clean()
        except ValidationError as e:
            return JsonResponse({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        nova_cidade.save()
        return JsonResponse({'municipio': municipio_to_dict(nova_cidade)}, status=status.HTTP_201_CREATED)

@csrf_exempt
def municipio_detail(request, pk):
    try:
        cidade = Municipio.objects.get(pk=pk)
    except Municipio.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return JsonResponse({'municipio': municipio_to_dict(cidade)})

    elif request.method == 'DELETE':
        cidade.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        data = json.loads(request.body)

        cidade.nome = data.get('nome')

        if 'uf' in data:
            try:
                cidade.uf = Uf.objects.get(pk=data['uf'])
            except Uf.DoesNotExist:
                return JsonResponse({"erro": "UF inválida"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cidade.full_clean()
        except ValidationError as e:
            return JsonResponse({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        cidade.save()
        return JsonResponse({'municipio': municipio_to_dict(cidade)})

    
# Area Pesca
@csrf_exempt
def area_pesca_list(request):
    if request.method == 'GET':
        area_pesca = AreaPesca.objects.all()
        area_pesca_dicts = [area_pesca_to_dict(obs) for obs in area_pesca]
        return JsonResponse({'areas_pescas': area_pesca_dicts})
        
    elif request.method == 'POST':
        params = json.loads(request.body)
        nova_area_pesca = AreaPesca(descricao = params.get('descricao'))
        try:
            nova_area_pesca.full_clean()
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        nova_area_pesca.save()
        return JsonResponse({'area_pesca': area_pesca_to_dict(nova_area_pesca)}, status=status.HTTP_201_CREATED)
        
@csrf_exempt
def area_pesca_detail(request, pk):
    try:
        area_pesca = AreaPesca.objects.get(pk=pk)
    except AreaPesca.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return JsonResponse({'area_pesca': area_pesca_to_dict(area_pesca)})
        
    elif request.method == 'PUT':
        data = json.loads(request.body)

        area_pesca.descricao = data.get('descricao')

        try: 
            area_pesca.full_clean()
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
            
        area_pesca.save()
        return JsonResponse({'area_pesca': area_pesca_to_dict(area_pesca)})
        
    elif request.method == 'DELETE':
        area_pesca.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

# Arte Pesca
@csrf_exempt
def arte_pesca_list(request):
    if request.method == 'GET':
        arte_pesca = ArtePesca.objects.all()
        area_pesca_dicts = [arte_pesca_to_dict(obs) for obs in arte_pesca]
        return JsonResponse({'arte_pesca': area_pesca_dicts})
        
    elif request.method == 'POST':
        params = json.loads(request.body)
        nova_arte_pesca = ArtePesca(nome = params.get('nome'))
        try:
            nova_arte_pesca.full_clean()
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        nova_arte_pesca.save()
        return JsonResponse({'arte_pesca': arte_pesca_to_dict(nova_arte_pesca)}, status=status.HTTP_201_CREATED)

@csrf_exempt
def arte_pesca_detail(request, pk):
    try:
        arte_pesca = ArtePesca.objects.get(pk=pk)
    except ArtePesca.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return JsonResponse({'arte_pesca': arte_pesca_to_dict(arte_pesca)})
    
    elif request.method == 'PUT':
        data = json.loads(request.body)

        arte_pesca.nome = data.get('nome')

        try:
            arte_pesca.full_clean()
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        arte_pesca.save()
        return JsonResponse({'arte_pesca': arte_pesca_to_dict(arte_pesca)})
    elif request.method == 'DELETE':
        arte_pesca.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

def estado_to_dict(estado: Uf) -> dict:
    """Converter um objeto Uf em um dicionário"""
    return {
        'id': estado.id,
        'nome': estado.nome,
        'sigla': estado.sigla
    }

def municipio_to_dict(municipio: Municipio) -> dict:
    return {
        'id': municipio.id,
        'nome': municipio.nome,
        'uf': municipio.uf.id,
    }

def area_pesca_to_dict(area_pesca: AreaPesca) -> dict:
    return {
        'id': area_pesca.id,
        'descricao': area_pesca.descricao,
    }

def arte_pesca_to_dict(arte_pesca: ArtePesca) -> dict:
    return {
        'id': arte_pesca.id,
        'nome': arte_pesca.nome,
    }