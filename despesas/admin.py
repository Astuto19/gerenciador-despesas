from django.contrib import admin
from .models import Despesa

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'usuario')