from django.db import models
from django.contrib.auth.models import User
from datetime import date 

class Despesa(models.Model):
    CATEGORIAS = [
        ('ALIMENTACAO', 'Alimentação'),
        ('TRANSPORTE', 'Transporte'),
        ('MORADIA', 'Moradia'),
        ('LAZER', 'Lazer'),
        ('OUTROS', 'Outros'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
    
    @property
    def esta_atrasada(self):
        # É atrasada se: A data é menor que hoje E não foi paga
        return self.data < date.today() and not self.pago