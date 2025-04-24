from rest_framework import serializers
from .models import Uf, Municipio, AreaPesca, ArtePesca


class UfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uf
        fields = ['id', 'nome', 'sigla']


class MunicipioSerializer(serializers.ModelSerializer):
    uf = serializers.PrimaryKeyRelatedField(queryset=Uf.objects.all())

    class Meta:
        model = Municipio
        fields = ['id', 'nome', 'uf']


class AreaPescaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaPesca
        fields = ['id', 'descricao']


class ArtePescaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtePesca
        fields = ['id', 'nome']
