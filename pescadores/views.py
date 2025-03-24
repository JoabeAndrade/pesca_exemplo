from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Uf, Municipio
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
            return JsonResponse({}, status=400)
        novo_estado.save()
        return JsonResponse({'uf': estado_to_dict(novo_estado)}, status=201)

@csrf_exempt
def uf_detail(request, pk):
    try:
        estado = Uf.objects.get(pk=pk)
    except Uf.DoesNotExist:
        return JsonResponse({}, status=404)

    if request.method == 'GET':
        return JsonResponse({'uf': estado_to_dict(estado)})

    elif request.method == 'DELETE':
        estado.delete()
        return JsonResponse({}, status=204)

    elif request.method == 'PUT':
        data = json.loads(request.body)

        estado.nome = data.get('nome')
        estado.sigla = data.get('sigla')

        try:
            estado.full_clean()
        except ValidationError:
            return JsonResponse({}, status=400)

        estado.save()
        return JsonResponse({'uf': estado_to_dict(estado)})

# Municipios
@csrf_exempt
def municipio_list(request):
    if request.method == 'GET':
        municipios = Municipio.objects.all()
        municipios_list = [municipio_to_dict(mun) for mun in municipios]
        return JsonResponse({'municipios': municipios_list}, status=200)
    
    elif request.method == 'POST':
        params = json.loads(request.body)
        uf_id = params.get('uf')
        try:
            uf = Uf.objects.get(pk=uf_id)
        except Uf.DoesNotExist:
            return JsonResponse({"erro": "Uf inválida"}, status=400)
        
        nova_cidade = Municipio(nome=params.get('nome'), uf=uf)

        try:
            nova_cidade.full_clean()
        except ValidationError as e:
            return JsonResponse({"erro": str(e)}, status=400)
        nova_cidade.save()
        return JsonResponse({'municipio': municipio_to_dict(nova_cidade)}, status=201)

@csrf_exempt
def municipio_detail(request, pk):
    try:
        cidade = Municipio.objects.get(pk=pk)
    except Municipio.DoesNotExist:
        return JsonResponse({}, status=404)

    if request.method == 'GET':
        return JsonResponse({'municipio': municipio_to_dict(cidade)})

    elif request.method == 'DELETE':
        cidade.delete()
        return JsonResponse({}, status=204)

    elif request.method == 'PUT':
        data = json.loads(request.body)

        cidade.nome = data.get('nome')

        if 'uf' in data:
            try:
                cidade.uf = Uf.objects.get(pk=data['uf'])
            except Uf.DoesNotExist:
                return JsonResponse({"erro": "UF inválida"}, status=400)
        
        try:
            cidade.full_clean()
        except ValidationError as e:
            return JsonResponse({"erro": str(e)}, status=400)
        
        cidade.save()
        return JsonResponse({'municipio': municipio_to_dict(cidade)})

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
