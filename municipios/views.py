from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Uf
import json

@csrf_exempt
def uf_list(request):
    if request.method == 'GET':
        estados = Uf.objects.all()
        estado_dicts = [estado_to_dict(obs) for obs in estados]
        return JsonResponse({"ufs": estado_dicts})

    elif request.method == 'POST':
        response = json.loads(request.body)
        novo_estado = Uf(nome=response['nome'], sigla=response['sigla'])
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

    elif request.method == 'PUT' or request.method == 'PATCH':
        response = json.loads(request.body)
        if 'nome' in response:
            estado.nome = response['nome']
        if 'sigla' in response:
            estado.sigla = response['sigla']
        estado.save()
        return JsonResponse({'uf': estado_to_dict(estado)})

def estado_to_dict(estado: Uf) -> dict:
    """Converter um objeto Uf em um dicionário"""
    return {
        'id': estado.id,
        'nome': estado.nome,
        'sigla': estado.sigla
    }
