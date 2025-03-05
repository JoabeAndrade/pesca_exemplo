from django.db import models

class Uf(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2)

class Municipio(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.ForeignKey(Uf, on_delete=models.PROTECT)
