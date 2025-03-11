from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Uf, Municipio
import json

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

def municipio_list(request):
    if request.method == 'GET':
        municipios = Municipio.objects.all()
        municipios_list = [municipio_to_dict(mun) for mun in municipios]
        return JsonResponse({'municipios': municipios_list}, status=200)

def municipio_detail(request, pk):
    ...

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
