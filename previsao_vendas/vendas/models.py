from statistics import mode
from django.db import models


class Venda(models.Model):
    onde_comprou = models.CharField(verbose_name='Onde Comprou', max_length=20)
    genero = models.CharField(verbose_name='Gênero', max_length=20)
    tipo_roupa = models.CharField(verbose_name='Tipo de Roupa', max_length=40)
    cor = models.CharField(verbose_name='Cor', max_length=40)
    tamanho = models.CharField(verbose_name='Tamanho', max_length=10)
    preco = models.FloatField(verbose_name='Preço')
    estacao = models.CharField(verbose_name='Estação', max_length=10)
    mes = models.CharField(verbose_name='Mês', max_length=15)
