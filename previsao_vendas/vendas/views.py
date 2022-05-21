from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Venda

import json
import pandas as pd
import numpy as np 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def index(request):
    vendas = Venda.objects.values()
    
    paginator = Paginator(vendas, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request, 
        'vendas/index.html', 
        {'vendas': page_obj}
    )


def create(request):
    return render(request, 'vendas/create.html')


def store(request):
    registro = Venda()
    try:
        registro.onde_comprou = request.POST.get('onde_comprou')
        registro.genero = request.POST.get('genero')
        registro.tipo_roupa = request.POST.get('tipo_roupa')
        registro.cor = request.POST.get('cor')
        registro.tamanho = request.POST.get('tamanho')
        registro.preco = request.POST.get('preco')
        registro.estacao = request.POST.get('estacao')
        registro.mes = request.POST.get('mes')
        
        registro.save()
        messages.add_message(request, messages.SUCCESS, 'Registro salvo com sucesso!')

    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar salvar o registro')
    
    return redirect('vendas:vendas_index')


def edit(request, id):
    data = get_object_or_404(Venda, id=id)
    return render(request, 'vendas/edit.html', {'data': data})


def update(request, id):
    registro = get_object_or_404(Venda, id=id)
    try:
        registro.onde_comprou = request.POST.get('onde_comprou')
        registro.genero = request.POST.get('genero')
        registro.tipo_roupa = request.POST.get('tipo_roupa')
        registro.cor = request.POST.get('cor')
        registro.tamanho = request.POST.get('tamanho')
        registro.preco = request.POST.get('preco')
        registro.estacao = request.POST.get('estacao')
        registro.mes = request.POST.get('mes')
        
        registro.save()
        messages.add_message(request, messages.SUCCESS, 'Registro atualizado com sucesso!')

    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar atualizar o registro.')

    return redirect('vendas:vendas_index')


def delete(request, id):
    registro = get_object_or_404(Venda, id=id)
    registro.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro deletado com sucesso!')
    return redirect('vendas:vendas_index')


def charts(request):
    vendas = Venda.objects.all()
    
    if(not vendas):
        messages.add_message(request, messages.ERROR, 'Banco de dados vazio.')
        return redirect('vendas:vendas_index')
    
    vendas_json = queryset_to_json(vendas)
    df = pd.read_json(vendas_json)
    
    data = {}
        
    df_fem = df.loc[df['genero'] == 'Feminino']
    df_masc = df.loc[df['genero'] == 'Masculino']

    # Vendas por tipo de roupa
    rotulos_tipo_roupa = list(df['tipo_roupa'].unique())
    
    qtd_feminino_tipo_roupa = [(df_fem['tipo_roupa'] == tam).sum() for tam in rotulos_tipo_roupa]
    qtd_masculino_tipo_roupa = [(df_masc['tipo_roupa'] == tam).sum() for tam in rotulos_tipo_roupa]
    
    rotulos_tipo_roupa = json.dumps(rotulos_tipo_roupa)
    data['qtd_tipo_roupa'] = [rotulos_tipo_roupa, qtd_feminino_tipo_roupa, qtd_masculino_tipo_roupa]


    # Vendas por tamanho
    rotulos_tamanho = ['PP', 'P', 'M', 'G', 'GG', 'EX']
    
    qtd_feminino_tamanho = [(df_fem['tamanho'] == tam).sum() for tam in rotulos_tamanho]
    qtd_masculino_tamanho = [(df_masc['tamanho'] == tam).sum() for tam in rotulos_tamanho]
    
    rotulos_tamanho = json.dumps(rotulos_tamanho)
    data['qtd_tamanho'] = [rotulos_tamanho, qtd_feminino_tamanho, qtd_masculino_tamanho]
    
    # Vendas por cores
    rotulos_cor = df['cor'].unique()
    qtd_feminino_cor = [(df_fem['cor'] == cor).sum() for cor in rotulos_cor]
    qtd_masculino_cor = [(df_masc['cor'] == cor).sum() for cor in rotulos_cor]

    rotulos_cor = json.dumps(list(rotulos_cor))
    data['qtd_cor'] = [rotulos_cor, qtd_feminino_cor, qtd_masculino_cor]
    
    # Tipo de loja
    rotulos_loja = df['onde_comprou'].unique()
    
    qtd_tipo_loja = [df.loc[df['onde_comprou'] == loja]['preco'].sum() for loja in rotulos_loja]
    # Passando para porcentagem
    total = qtd_tipo_loja[0] + qtd_tipo_loja[1]
    qtd_tipo_loja[0] = round((qtd_tipo_loja[0]) / total * 100, 1)
    qtd_tipo_loja[1] = 100 - qtd_tipo_loja[0]
    
    data['qtd_tipo_loja'] = qtd_tipo_loja
    
    # Vendas por gênero
    rotulos_genero = ['Feminino', 'Masculino']
    
    qtd_genero = [df.loc[df['genero'] == genero]['preco'].sum() for genero in rotulos_genero]
    # Passando para porcentagem
    total = qtd_genero[0] + qtd_genero[1]
    qtd_genero[0] = round((qtd_genero[0]) / total * 100, 1)
    qtd_genero[1] = 100 - qtd_genero[0]

    data['qtd_genero'] = qtd_genero
    
    # Dinheiro total por mês
    rotulos_mes = df['mes'].unique()
    
    qtd_dinheiro_mes = [df.loc[df['mes'] == mes]['preco'].sum() for mes in rotulos_mes]
    
    rotulos_mes = json.dumps(list(rotulos_mes))
    data['qtd_dinheiro_mes'] = [rotulos_mes, qtd_dinheiro_mes]
    
    
    # Previsão --------------------------------------------------------
    meses = df['mes'].unique()
    x = np.arange(1, len(meses)+1) #cria um array que vai do numero 1 ao tamanho de meses + 1
    x = x[:, np.newaxis] #faz o array 1D virar 2D
    y = np.array([df.loc[df['mes'] == mes]['preco'].sum() for mes in meses]) #lista do lucro obtido em cada mês

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state = 0) #35% de dados para teste

    # Produz um modelo de regressão linear
    model = LinearRegression()
    model.fit(x_train, y_train) #treina o modelo

    x_fit = np.linspace(1, len(meses)+2) #quantidade de meses no eixo X
    x_fit = x_fit[:, np.newaxis] #faz o array 1D virar 2D
    y_fit = model.predict(x_fit) #preve os valores de cada posicao no eixo Y

    # Pegando a primeira e última coordenada de fit
    fit_start_x = int(x_fit[0][0])
    fit_start_y = y_fit[0]
    fit_end_x = int(x_fit[-1][0])
    fit_end_y = y_fit[-1]
    data['fit_border_coords'] = [fit_start_x, fit_start_y, fit_end_x, fit_end_y]
    
    # Pegando as coordenadas de train
    train_coords = []
    for i in range(len(x_train)):
        train_coords.append([x_train[i][0], y_train[i]])
    
    data['train_coords'] = train_coords
    
    # Pegando as coordenadas de test
    test_coords = []
    for i in range(len(x_test)):
        test_coords.append([x_test[i][0], y_test[i]])
    
    data['test_coords'] = test_coords
    
    return render(
        request,
        'vendas/charts.html',
        {'data': data}
    )


def queryset_to_json(query_set):
    results = {
        'onde_comprou': [],
        'genero': [],
        'tipo_roupa': [],
        'cor': [],
        'tamanho': [],
        'preco': [],
        'estacao': [],
        'mes': [],
    }
    
    for result in query_set:
        results['onde_comprou'].append(result.onde_comprou)
        results['genero'].append(result.genero)
        results['tipo_roupa'].append(result.tipo_roupa)
        results['cor'].append(result.cor)
        results['tamanho'].append(result.tamanho)
        results['preco'].append(float(result.preco))
        results['estacao'].append(result.estacao)
        results['mes'].append(result.mes)
    
    return json.dumps(results)
