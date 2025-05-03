# ---------------------------------------------
# Dashboard de Análise de Sinistros de Trânsito
# ---------------------------------------------
#
# Finalidade:
# Este código implementa um dashboard interativo em Streamlit para análise de acidentes de trânsito na cidade do Recife, utilizando dados históricos da CTTU (2016-2024).
# O sistema permite filtrar, visualizar e explorar dados de acidentes, além de recomendar rotas mais seguras com base em um modelo de machine learning.
#
# Funcionalidades:
# - Unificação automática de arquivos CSV anuais de acidentes.
# - Filtros interativos por tipo de acidente e intervalo de datas.
# - Visualizações: totais, gráficos por ano, mês, bairro, mapa de calor.
# - Recomendação de rotas seguras baseada em classificação de risco por bairro.
#
# Como usar:
# 1. Coloque todos os arquivos acidentes*.csv na mesma pasta do script.
# 2. Execute o script com: streamlit run dash_cttu_novo.py
# 3. Utilize os filtros e explore as visualizações.
#
# Autor: Faculdade SENAC - PE / MBA Ciência de Dados e IA / Prof. Geraldo Gomes / Agosto 2024
# ---------------------------------------------

# 1. IMPORTAR BIBLIOTECAS

import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import networkx as nx
import matplotlib.pyplot as plt
import glob
import os

# 2. CONFIGURAÇÃO DA PÁGINA

st.set_page_config(page_title="Dashboard", layout="wide")

# 3. TÍTULO DASHBOARD

with st.container():
    st.write("<h4 style='color:green; font-size:20px;'> Faculdade SENAC - PE * MBA Ciência de Dados e IA * Linguagem Python (Prof. Geraldo Gomes) * Agosto 2024</h4>", 
    unsafe_allow_html=True)
    st.title("Análise de Sinistros de Trânsito - Cidade do Recife")
    st.write("Série histórica: 2016 a 2024")
    st.write("Fonte: Autarquia de Trânsito e Transporte Urbano do Recife - CTTU")
    st.write("Quer acessar a fonte de dados?  [Clique aqui](https://dados.recife.pe.gov.br/pt_PT/dataset/acidentes-de-transito-com-e-sem-vitimas)")
      
# 4. CARREGAMENTO E TRATAMENTO

with st.container():
    st.write("---")
    # Unificar todos os arquivos CSV da pasta
    csv_files = glob.glob(os.path.join(os.path.dirname(__file__), 'acidentes*.csv'))
    df_list = []
    for file in csv_files:
        # Detectar separador automaticamente
        with open(file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            sep = ';' if first_line.count(';') > first_line.count(',') else ','
        df = pd.read_csv(file, delimiter=sep)
        df_list.append(df)
    dados = pd.concat(df_list, ignore_index=True)
    dados['data'] = pd.to_datetime(dados['data'])

    # Adicionar colunas de Latitude e Longitude já no tratamento inicial
    coordenadas_bairros = {
        'BOA VIAGEM': (-8.1192, -34.9041),
        'IMBIRIBEIRA': (-8.1127, -34.9187),
        'DERBY': (-8.0626, -34.8871),
        'ILHA DO RETIRO': (-8.0586, -34.9022),
        'ESPINHEIRO': (-8.0377, -34.8986),
        'TORRE': (-8.0372, -34.9157),
        'ARRUDA': (-8.0272, -34.8857),
        'CASA FORTE': (-8.0276, -34.9077),
        'GRAÇAS': (-8.0456, -34.8982),
        'SANTO AMARO': (-8.0539, -34.8817),
        'MADALENA': (-8.0452, -34.9172),
        'PINA': (-8.1042, -34.8817),
        'AFOGADOS': (-8.0736, -34.9182),
        'CORDEIRO': (-8.0457, -34.9362),
        'VÁRZEA': (-8.0341, -34.9522),
        'JAQUEIRA': (-8.0347, -34.8942),
        'ENCRUZILHADA': (-8.0332, -34.8852),
        'CAMPO GRANDE': (-8.0702, -34.9002),
        'SANTO ANTÔNIO': (-8.0632, -34.8732),
        'SÃO JOSÉ': (-8.0672, -34.8722),
        # ...adicione mais bairros conforme necessário...
    }
    # Padronizar nome da coluna de bairro para 'uf_cidade_bairro' se necessário
    possiveis_nomes_bairro = ['uf_cidade_bairro', 'bairro', 'local_bairro', 'bairro_ocorrencia', 'bairro_nome']
    nome_bairro = None
    for nome in possiveis_nomes_bairro:
        if nome in dados.columns:
            nome_bairro = nome
            break
    if nome_bairro and nome_bairro != 'uf_cidade_bairro':
        dados['uf_cidade_bairro'] = dados[nome_bairro]
    elif 'uf_cidade_bairro' not in dados.columns:
        dados['uf_cidade_bairro'] = None
    # Criar as colunas Latitude e Longitude
    dados['Latitude'] = dados['uf_cidade_bairro'].map(lambda x: coordenadas_bairros.get(str(x).strip().upper(), (None, None))[0] if pd.notnull(x) else None)
    dados['Longitude'] = dados['uf_cidade_bairro'].map(lambda x: coordenadas_bairros.get(str(x).strip().upper(), (None, None))[1] if pd.notnull(x) else None)

    # Exibindo as colunas como uma tabela
    #st.write(pd.DataFrame(dados.columns, columns=["Colunas"]))

# 5. CRIANDO UM MENU LATERAL
    
    # Adicionar imagem acima do nome "Filtros"
    st.sidebar.image("https://i.postimg.cc/Y9r35LCg/Logo-1.png", width=250)
    
    # Barra - marcador
    st.sidebar.header("Filtros")  

    # Filtro tipo de acidentes
    tipos_unicos = dados['tipo'].unique()
    tipo_acid = st.sidebar.multiselect("Escolha o tipo do acidente", tipos_unicos)

    # Obter a data mínima e máxima após a conversão correta para datetime
    dt_inicio = dados['data'].min().to_pydatetime()
    dt_fim = dados['data'].max().to_pydatetime()
    # Criar o slider de intervalo de datas com valores do tipo datetime
    intervalo_datas = st.sidebar.slider(
        "Selecione o intervalo de datas",
        min_value=dt_inicio,
        max_value=dt_fim,
        value=(dt_inicio, dt_fim)
    )
    # Aplicar o filtro de datas nos dados
    dados = dados[(dados['data'] >= intervalo_datas[0]) & (dados['data'] <= intervalo_datas[1])]

    # Aplica filtro aos dados
    if tipo_acid:
        dados = dados[dados['tipo'].isin(tipo_acid)]

    st.sidebar.write("---")
    
    # Barra - marcador
    st.sidebar.header("Equipe")  

    # Adicionar imagem acima do nome "Filtros"
    st.sidebar.image("https://i.postimg.cc/7ZPSYrk8/Equipe.png", width=200)

# 6. PRÉ-PROCESSAMENTO

    # Remove colunas 100% sem dados
    dados = dados.dropna(axis=1, how='all')
    # Função para formatar números com separador de milhar
    def format_number(number):
        try:
            return "{:,.0f}".format(float(number)).replace(',', '.')
        except (ValueError, TypeError):
            return number  # Retorna o valor original se ocorrer um erro
    # Convertendo texto para números inteiros
    dados['vitimas'] = pd.to_numeric(dados['vitimas'], errors='coerce')
    dados['vitimasfatais'] = pd.to_numeric(dados['vitimasfatais'], errors='coerce')
    # Calcular totais
    total_vitimas = dados['vitimas'].sum()
    total_vitimas_fatais = dados['vitimasfatais'].sum()
    total_ocorrencias = dados['data'].count()
    # Criar colunas
    col1, col2, col3 = st.columns(3)
    # Formatação dos números
    col1.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Total de Ocorrências</h2><p style='font-size: 50px;'>{format_number(total_ocorrencias)}</p>", unsafe_allow_html=True)
    col2.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Total de Vítimas</h2><p style='font-size: 50px;'>{format_number(total_vitimas)}</p>", unsafe_allow_html=True)
    col3.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Total de Vítimas Fatais</h2><p style='font-size: 50px;'>{format_number(total_vitimas_fatais)}</p>", unsafe_allow_html=True)

# 7. AGREGAÇÕES E DATA VISUALIZATION

    st.write("---")

    # Total de ocorrências por ano (Gráfico de Barras Vertical)
    st.write("Total de Ocorrências por Ano")
    dados['ano'] = dados['data'].dt.year
    ocorrencias_por_ano = dados.groupby('ano')['data'].count().reset_index()
    ocorrencias_por_ano.columns = ['Ano', 'Total de Ocorrências']
    fig_barras = px.bar(ocorrencias_por_ano, x='Ano', y='Total de Ocorrências',
                    labels={'Total de Ocorrências': 'Total de Ocorrências'},
                    text_auto=True,color_discrete_sequence=['#0958D9'])
    st.plotly_chart(fig_barras, use_container_width=True)
    st.write("Insights:")
    st.write("1. Conforme a análise do conjunto de dados, o ano com mais sinistros de trânsito é o de 2019;")
    st.write("2. Podemos ver uma baixa significativa de acidentes depois do ano de 2019.")

    st.write("---")

   
        
    # Total de ocorrência por mês (Gráfico de Barras Vertical)
    st.write("Total de Ocorrências por Mês")
    dados['mes'] = dados['data'].dt.month  # Extrair o mês a partir da data
    ocorrencias_por_mes = dados.groupby('mes')['data'].count().reset_index()
    fig_mes = px.bar(ocorrencias_por_mes, x='mes', y='data', labels={'data': 'Total de Ocorrências', 'mes': 'Mês'}, 
                     text_auto=True, color_discrete_sequence=['#0958D9'])
    fig_mes.update_layout(xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                  'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    ))  # Ajustando o rótulo do eixo x para exibir os nomes dos meses
    st.plotly_chart(fig_mes)  # Exibir o gráfico no Streamlit
    st.write("Insights:")
    st.write("1. Os meses de Junho e Julho são os menores meses de acidentes de trânsito;")
    st.write("2. Tanto o os meses iniciais como os finais, são o que apresentam os maiores números de acidentes.")

    st.write("---")
    
    # Total de ocorrência por bairro (Top 10 - Gráfico de Barras Horizontal)
    st.write("Top 10 Bairros com Mais Ocorrências")
    ocorrencias_por_bairro = dados.groupby('bairro')['data'].count().reset_index()  # Agrupar dados por bairro e calcular o total de ocorrências
    top_10_bairros = ocorrencias_por_bairro.sort_values(by='data', ascending=False).head(10)  # Ordenar por número de ocorrências e selecionar o top 10
    fig_top_10 = px.bar(top_10_bairros,  # Criar gráfico de barras horizontal
                        x='data', 
                        y='bairro', 
                        orientation='h',  # Define o gráfico como horizontal
                        labels={'data': 'Total de Ocorrências', 'bairro': 'Bairro'},
                        text='data',    # Adiciona os rótulos dos valores
                        color_discrete_sequence=['#0958D9'])  # Define a cor do gráfico
    fig_top_10.update_layout(yaxis={'categoryorder': 'total ascending'}, 
                             xaxis_title="Total de Ocorrências",
                             yaxis_title="Bairro")  # Ajustar layout para melhorar a visualização
    st.plotly_chart(fig_top_10)  # Exibir o gráfico no Streamlit
    st.write("Insights:")
    st.write("1. Imbiribeira e Boa Viagem lideram com os maiores números de acidentes.")
    st.write("2. ")
    st.write("3. ")

    st.write("---")
    
    # Comparativo Total de Vitimas vs Total de Vitimas Fatais (Grafico de Linhas multiplas)
    with st.container():
        st.write("Comparação entre Total de Vítimas e Vítimas Fatais por Mês")
        anos_disponiveis = sorted(dados['data'].dt.year.unique())  # Extrair e ordenar os anos disponíveis para o slicer
        anos_selecionados = st.multiselect('Selecione os Anos', anos_disponiveis, default=anos_disponiveis, key='anos_selecionados_1')  # Adicionar o slicer para selecionar múltiplos anos
        dados_filtrados = dados[dados['data'].dt.year.isin(anos_selecionados)]  # Filtrar os dados com base nos anos selecionados
        vitimas_por_mes = dados_filtrados.groupby(dados_filtrados['data'].dt.strftime('%b'))[['vitimas', 'vitimasfatais']].sum().reset_index()  # Calcular o total de vítimas e vítimas fatais por mês
        vitimas_por_mes = vitimas_por_mes.sort_values(by='data')  # Ordenar os meses
        fig_vitimas = go.Figure()
        fig_vitimas.add_trace(go.Scatter(x=vitimas_por_mes['data'], y=vitimas_por_mes['vitimas'],
                                        mode='lines+markers+text', name='Total de Vítimas',
                                        text=vitimas_por_mes['vitimas'], textposition='top center',
                                        line=dict(color='#0958D9')))
        fig_vitimas.add_trace(go.Scatter(x=vitimas_por_mes['data'], y=vitimas_por_mes['vitimasfatais'],
                                        mode='lines+markers+text', name='Total de Vítimas Fatais',
                                        text=vitimas_por_mes['vitimasfatais'], textposition='top center',
                                        line=dict(color='green')))
        fig_vitimas.update_layout(xaxis_title="Mês", yaxis_title="Total", 
                                xaxis=dict(
                                    tickmode='array',
                                    tickvals=np.arange(1, 13),
                                    ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun','Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']))
        st.plotly_chart(fig_vitimas, use_container_width=True) # Exibir o gráfico em widescreen
    st.write("Insights:")
    st.write("1. O mês de Setembro lidera com o número total de vítimas em todos os anos;")
    st.write("2. O mês de Fevereiro é o maior com vítimas fatais em todos os anos.")

    st.write("---")

    # Mapa de calor mostrando o total de ocorrências por bairro
    st.write("Mapa de Calor - Total de Ocorrências por Bairro")
    if 'Latitude' in dados.columns and 'Longitude' in dados.columns:
        dados = dados.dropna(subset=['Latitude', 'Longitude']) # Remover linhas onde a latitude ou longitude estão ausentes
        mapa = folium.Map(location=[-8.0476, -34.8770], zoom_start=12)
        heat_data = [[row['Latitude'], row['Longitude']] for index, row in dados.iterrows()]
        HeatMap(heat_data).add_to(mapa) # Criar o mapa de calor
        folium_static(mapa) # Renderizar o mapa no Streamlit   
        st.write("Insights:")
        st.write("1. Segundo o nosso conjunto de dados, nota-se que no bairro em Boa Viagem há uma alta concentração de acidentes de transitos;")
        st.write("2. Podemos ver também que há uma concentração de acidentes na imediações da Av. Agamenon Magalhâes, próximos aos bairros do Derby e da Ilha do Retiro;")
        st.write("3. O Mesmo comportamento acontece nos bairros do Espinheiro, Torre e Arruda.")
    else:
        st.warning("Colunas 'Latitude' e 'Longitude' não encontradas nos dados. O mapa de calor não será exibido.")
    st.write("---")

# 8. APLICAÇÃO MODELO DE MACHINE LEARNING

    # Construir um modelo de Machine Learning no qual os retornos sejam recomendações de rotas seguras através da inserção (get)
    # do ponto A (origem) ao ponto B (destino), considerando a quantidade de ocorrências por localidade. A recomendação visa evitar
    # rotas nas quais exista maior probabilidade de acontecer sinistros 

    # Título da aplicação
    st.title("Recomendação de Rota")
    # Verificar se as colunas de latitude e longitude estão presentes
    if 'Latitude' not in dados.columns or 'Longitude' not in dados.columns:
        st.error("As colunas 'Latitude' e 'Longitude' não estão presentes no arquivo consolidado.")
    else:
        
        # Padronizar nome da coluna de bairro para 'uf_cidade_bairro'
        possiveis_nomes_bairro = ['uf_cidade_bairro', 'bairro', 'local_bairro', 'bairro_ocorrencia', 'bairro_nome']
        nome_bairro = None
        for nome in possiveis_nomes_bairro:
            if nome in dados.columns:
                nome_bairro = nome
                break
        if nome_bairro and nome_bairro != 'uf_cidade_bairro':
            dados['uf_cidade_bairro'] = dados[nome_bairro]
        elif 'uf_cidade_bairro' not in dados.columns:
            st.error("Coluna de bairro não encontrada nos dados. As análises por bairro não funcionarão.")

        # Dicionário de coordenadas dos bairros do Recife (todas as chaves em caixa alta)
        coordenadas_bairros = {
            'BOA VIAGEM': (-8.1192, -34.9041),
            'IMBIRIBEIRA': (-8.1127, -34.9187),
            'DERBY': (-8.0626, -34.8871),
            'ILHA DO RETIRO': (-8.0586, -34.9022),
            'ESPINHEIRO': (-8.0377, -34.8986),
            'TORRE': (-8.0372, -34.9157),
            'ARRUDA': (-8.0272, -34.8857),
            'CASA FORTE': (-8.0276, -34.9077),
            'GRAÇAS': (-8.0456, -34.8982),
            'SANTO AMARO': (-8.0539, -34.8817),
            'MADALENA': (-8.0452, -34.9172),
            'PINA': (-8.1042, -34.8817),
            'AFOGADOS': (-8.0736, -34.9182),
            'CORDEIRO': (-8.0457, -34.9362),
            'VÁRZEA': (-8.0341, -34.9522),
            'JAQUEIRA': (-8.0347, -34.8942),
            'ENCRUZILHADA': (-8.0332, -34.8852),
            'CAMPO GRANDE': (-8.0702, -34.9002),
            'SANTO ANTÔNIO': (-8.0632, -34.8732),
            'SÃO JOSÉ': (-8.0672, -34.8722),
            # ...adicione mais bairros conforme necessário...
        }
        # Adicionar Latitude e Longitude conforme o bairro (convertendo para caixa alta)
        dados['Latitude'] = dados['uf_cidade_bairro'].map(lambda x: coordenadas_bairros.get(str(x).strip().upper(), (None, None))[0])
        dados['Longitude'] = dados['uf_cidade_bairro'].map(lambda x: coordenadas_bairros.get(str(x).strip().upper(), (None, None))[1])

        # Só remove linhas se as colunas existirem
        if 'Latitude' in dados.columns and 'Longitude' in dados.columns:
            dados = dados.dropna(subset=['Latitude', 'Longitude'])

        # Padronizar nomes de latitude e longitude
        possiveis_lat = ['Latitude', 'latitude', 'lat', 'LATITUDE']
        possiveis_long = ['Longitude', 'longitude', 'long', 'lng', 'LONGITUDE']
        nome_lat = None
        nome_long = None
        for nome in possiveis_lat:
            if nome in dados.columns:
                nome_lat = nome
                break
        for nome in possiveis_long:
            if nome in dados.columns:
                nome_long = nome
                break
        if nome_lat and nome_lat != 'Latitude':
            dados['Latitude'] = dados[nome_lat]
        if nome_long and nome_long != 'Longitude':
            dados['Longitude'] = dados[nome_long]
        if 'Latitude' not in dados.columns or 'Longitude' not in dados.columns:
            st.error("Colunas de Latitude e/ou Longitude não encontradas nos dados. O mapa de calor não funcionará.")
        
        # Agrupar os dados por 'bairro' e contar o total de ocorrências em cada localidade
        df_agrupado = dados.groupby(['bairro', 'Latitude', 'Longitude']).size().reset_index(name='total_ocorrencias')
        # Classificar as localidades com base no total de ocorrências
        df_agrupado['classificacao'] = pd.cut(df_agrupado['total_ocorrencias'], # Considerar outras variaveis como: Número de vitimas
                                            bins=[0, 200, 500, float('inf')],
                                            labels=['Segura', 'Perigoso', 'Muito Perigoso'])
        

        # Dividir os dados em features (X) e rótulo (y)
        X = df_agrupado[['total_ocorrencias']]
        y = df_agrupado['classificacao']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Dividir em conjuntos de treinamento e teste
        modelo = RandomForestClassifier(n_estimators=100, random_state=42)  # Treinar o modelo
        modelo.fit(X_train, y_train)
        # Seção de input para os pontos A e B
        st.subheader("Informe os pontos de origem e destino")
        ponto_A = st.selectbox("Selecione o ponto de origem", df_agrupado['bairro'].unique())
        ponto_B = st.selectbox("Selecione o ponto de destino", df_agrupado['bairro'].unique())
        # Simular o grafo (exemplo simples)
        G = nx.Graph()
        # Adicionar arestas com base nos dados
        for _, row in df_agrupado.iterrows():
            # Adicionar arestas conectando cada localidade ao ponto central
            G.add_edge("Ponto Central", row['bairro'], weight=row['total_ocorrencias'])
        # Encontrar a rota mais segura de A para B
        try:
            rota_segura = nx.shortest_path(G, source=ponto_A, target=ponto_B, weight='weight')
            st.subheader("Rota Segura Recomendada")
            st.write(" -> ".join(rota_segura))
        except nx.NetworkXNoPath:
            st.error("Não foi possível encontrar uma rota entre os pontos selecionados.")
        # Plotar o grafo
        st.subheader("Visualização do Grafo de Rotas")
        plt.figure(figsize=(12, 12))  # Ajuste o tamanho da figura
        pos = nx.spring_layout(G, seed=42)  # Adicione uma semente para layout reprodutível
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        st.pyplot(plt)

    # O usuário dará todos os atributos
    # Local
    # Hora
    # Vitimas
    # Veículo
    # Fazer uma claissificação de risco com base no deslocamento
    # Vendder para seguradora onde a claissificação afertará a apolice do seguro, no qual o trajeto e deslocamento dirário conta