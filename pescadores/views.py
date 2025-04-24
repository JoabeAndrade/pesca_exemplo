from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Uf, Municipio, AreaPesca, ArtePesca
from .serializers import UfSerializer, MunicipioSerializer, AreaPescaSerializer, ArtePescaSerializer


# Estados
@api_view(['GET', 'POST'])
def uf_list(request):
    if request.method == 'GET':
        estados = Uf.objects.all()
        serializer = UfSerializer(estados, many=True)
        return Response({'ufs': serializer.data})

    elif request.method == 'POST':
        serializer = UfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'uf': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def uf_detail(request, pk):
    try:
        estado = Uf.objects.get(pk=pk)
    except Uf.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UfSerializer(estado)
        return Response({'uf': serializer.data})

    elif request.method == 'PUT':
        serializer = UfSerializer(estado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'uf': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        estado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Municipios
@api_view(['GET', 'POST'])
def municipio_list(request):
    if request.method == 'GET':
        municipios = Municipio.objects.all()
        serializer = MunicipioSerializer(municipios, many=True)
        return Response({'municipios': serializer.data})

    elif request.method == 'POST':
        serializer = MunicipioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'municipio': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def municipio_detail(request, pk):
    try:
        municipio = Municipio.objects.get(pk=pk)
    except Municipio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MunicipioSerializer(municipio)
        return Response({'municipio': serializer.data})

    elif request.method == 'PUT':
        serializer = MunicipioSerializer(municipio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'municipio': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        municipio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Area Pesca
@api_view(['GET', 'POST'])
def area_pesca_list(request):
    if request.method == 'GET':
        areas = AreaPesca.objects.all()
        serializer = AreaPescaSerializer(areas, many=True)
        return Response({'areas_pescas': serializer.data})

    elif request.method == 'POST':
        serializer = AreaPescaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'area_pesca': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def area_pesca_detail(request, pk):
    try:
        area = AreaPesca.objects.get(pk=pk)
    except AreaPesca.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AreaPescaSerializer(area)
        return Response({'area_pesca': serializer.data})

    elif request.method == 'PUT':
        serializer = AreaPescaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'area_pesca': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Arte Pesca
@api_view(['GET', 'POST'])
def arte_pesca_list(request):
    if request.method == 'GET':
        artes = ArtePesca.objects.all()
        serializer = ArtePescaSerializer(artes, many=True)
        return Response({'arte_pesca': serializer.data})

    elif request.method == 'POST':
        serializer = ArtePescaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'arte_pesca': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def arte_pesca_detail(request, pk):
    try:
        arte = ArtePesca.objects.get(pk=pk)
    except ArtePesca.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtePescaSerializer(arte)
        return Response({'arte_pesca': serializer.data})

    elif request.method == 'PUT':
        serializer = ArtePescaSerializer(arte, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'arte_pesca': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        arte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
