from django.shortcuts import render, redirect, get_object_or_404  # <--- Adicione o redirect
from django.contrib.auth.decorators import login_required
from .models import Despesa
from .forms import DespesaForm  # <--- Importe o formulário que acabamos de criar
from django.db.models import Sum # <--- 1. Importe isso aqui no topo!
# Adicione esta importação no topo do arquivo, junto com as outras
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta



# --- NOVA FUNÇÃO DE REGISTRO ---
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Cria o usuário no banco
            return redirect('login') # Manda para a tela de login
    else:
        form = UserCreationForm() # Formulário vazio

    return render(request, 'registration/registro.html', {'form': form})
@login_required(login_url='/admin/')
@login_required
def lista_despesas(request):
    # 1. Descobrir qual mês o usuário quer ver
    hoje = date.today()
    mes_atual = int(request.GET.get('mes', hoje.month))
    ano_atual = int(request.GET.get('ano', hoje.year))

    # 2. Filtrar despesas APENAS daquele mês e ano
    despesas = Despesa.objects.filter(
        usuario=request.user, 
        data__month=mes_atual, 
        data__year=ano_atual
    ).order_by('data')

    total = despesas.aggregate(Sum('valor'))['valor__sum'] or 0

    # 3. Calcular data para os botões "Anterior" e "Próximo"
    data_base = date(ano_atual, mes_atual, 1)
    
    # Voltar 1 mês
    mes_passado = data_base - timedelta(days=1)
    # Avançar 1 mês (truque: somar 31 dias leva pro próximo mês garantido)
    proximo_mes = data_base + timedelta(days=31)

    # 4. Verificar se tem contas atrasadas (Notificação Geral)
    contas_atrasadas = Despesa.objects.filter(
        usuario=request.user, 
        pago=False, 
        data__lt=hoje
    ).count()

    contexto = {
        'despesas': despesas,
        'total': total,
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
        'ant_mes': mes_passado.month,
        'ant_ano': mes_passado.year,
        'prox_mes': proximo_mes.month,
        'prox_ano': proximo_mes.year,
        'contas_atrasadas': contas_atrasadas, # Para o alerta
    }

    return render(request, 'despesas/lista_despesas.html', contexto)

# --- NOVA FUNÇÃO ABAIXO ---
@login_required(login_url='/admin/')
def criar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            # commit=False diz: "Pausa! Não salva no banco ainda"
            nova_despesa = form.save(commit=False)
            # "Preencha o usuário com quem está logado agora"
            nova_despesa.usuario = request.user
            # "Agora sim, pode salvar"
            nova_despesa.save()
            return redirect('lista_despesas') # Volta para a lista
    else:
        form = DespesaForm() # Cria formulário vazio

    return render(request, 'despesas/form_despesa.html', {'form': form})

@login_required(login_url='/admin/')
def editar_despesa(request, pk):
    # Pega a despesa com esse ID, mas SÓ se for do usuário atual
    despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)

    if request.method == 'POST':
        # instance=despesa diz: "Não cria um novo, atualiza ESSE aqui"
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=despesa) # Preenche o formulário com os dados existentes

    # Reutilizamos o mesmo HTML de criar!
    return render(request, 'despesas/form_despesa.html', {'form': form})

@login_required(login_url='/admin/')
def excluir_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)

    if request.method == 'POST':
        despesa.delete()
        return redirect('lista_despesas')

    return render(request, 'despesas/confirmar_exclusao.html', {'despesa': despesa})