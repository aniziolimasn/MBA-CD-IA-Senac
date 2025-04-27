# ---------------------------------------------
# FINALIDADE DO CÓDIGO
# ---------------------------------------------
# Este código implementa um dashboard interativo utilizando Streamlit para análise das despesas do Estado de Pernambuco.
# O objetivo é consolidar, tratar e visualizar dados históricos de despesas públicas (2022-2024), permitindo filtragem por ano, modalidade, unidade gestora, função e subfunção.
# O dashboard apresenta indicadores, gráficos e tabelas para facilitar a compreensão dos gastos públicos, apoiando análises e tomadas de decisão.
# Fonte dos dados: SCGE - Secretaria da Controladoria-Geral do Estado de Pernambuco.
# ---------------------------------------------

# 1. IMPORTAR BIBLIOTECAS
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
import glob
 
# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Dashboard", layout="wide")
 
# CSS personalizado
st.markdown("""
    <style>
    /* Alterar a cor de fundo da barra lateral (filtros) */
    [data-testid="stSidebar"] {
        background-color: #1F537D;
    }
 
    /* Centralizar imagem na barra lateral */
    [data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
 
    /* Alterar cor de fundo da área principal */
    .main {
        background-color: #D2D5D8;
    }
 
    /* Centralizar texto da barra lateral */
    [data-testid="stSidebar"] .sidebar-content {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

 
# 3. CARREGAMENTO E TRATAMENTO
 
# Definir o caminho da pasta onde os arquivos .csv estão armazenados
caminho_csvs = r"G:\Projeto"
 
# Obter a lista de todos os arquivos .csv na pasta
arquivos_csv = glob.glob(os.path.join(caminho_csvs, "*.csv"))
 
# Lista para armazenar cada DataFrame
lista_dfs = []
 
# Ler todos os arquivos .csv e adicionar uma coluna 'ano'
for arquivo in arquivos_csv:
    try:
        # Ler o arquivo csv em um DataFrame com delimitador ";"
        df = pd.read_csv(arquivo, sep=';', on_bad_lines='skip')
 
        # Extrair o ano do nome do arquivo
        nome_arquivo = os.path.basename(arquivo)
        ano = nome_arquivo.split('.')[0]  # Supondo que o nome do arquivo é apenas o ano
       
        # Cria coluna 'ano' com o valor extraído
        df['ano'] = ano
       
        # Verificar se o DataFrame não está vazio antes de adicionar à lista
        if not df.empty:
            lista_dfs.append(df)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo {arquivo}: {e}")
 
# Realiza a união de todos os DataFrames em um único DataFrame consolidado
df_consolidado = pd.concat(lista_dfs, ignore_index=True)
 
# Remover colunas duplicadas, se houver
df_consolidado = df_consolidado.loc[:, ~df_consolidado.columns.duplicated()]

 
# Excluir as colunas indesejadas
colunas_a_excluir = ['cd_nm_subacao', 'obs', 'cd_nm_grupo',
                     'cd_nm_modalidade', 'cd_nm_elemento', 'cd_nm_item', 'cd_nm_item_vlrliquidado',
                     'vlrliquidado', 'vlrempenhado']
df_consolidado = df_consolidado.drop(columns=colunas_a_excluir, errors='ignore')
 
# Tratar a coluna vlrtotalpago
if 'vlrtotalpago' in df_consolidado.columns:
    # Limpar a coluna removendo caracteres indesejados e convertendo o formato
    df_consolidado['vlrtotalpago'] = df_consolidado['vlrtotalpago'].astype(str).str.replace('R\$', '', regex=False)  # Remove o símbolo de R$
    df_consolidado['vlrtotalpago'] = df_consolidado['vlrtotalpago'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)  # Formata para o padrão numérico

    # Converter os valores para float
    df_consolidado['vlrtotalpago'] = pd.to_numeric(df_consolidado['vlrtotalpago'], errors='coerce')  # Coerce para tratar erros
   
# 4. TÍTULO DASHBOARD
with st.container():
    st.write("<h4 style='color:green; font-size:20px;'> MBA Ciência de Dados e Inteligência Artificial </h4>", unsafe_allow_html=True)
    st.write("<h4 style='color:green; font-size:20px;'> Projeto Final Disciplina Visualização de Dados (Prof. Geraldo Gomes) * Setembro - Outubro 2024 </h4>", unsafe_allow_html=True)
    st.write("<h1 style='color:black;'>Análise das Despesas do Estado de Pernambuco</h1>", unsafe_allow_html=True)
    st.write("<h5 style='color:black;'>Série histórica: 2022 a 2024</h5>", unsafe_allow_html=True)
    st.write("<h5 style='color:black;'>Fonte: SCGE - Secretaria da Controladoria - Geral do Estado</h5>", unsafe_allow_html=True)
    st.write("<h9 style='color:black; font-style: italic;'>Órgão responsável por ampliar o controle do uso dos recursos e do patrimônio do Estado.</h9>", unsafe_allow_html=True)
    st.write("<h7 style='color:black;'>Quer acessar a fonte de dados? <a href='https://dados.pe.gov.br/dataset/todas-despesas-detalhadas' target='_blank'>Clique aqui</a></h7>", unsafe_allow_html=True)
 
    st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
 
    st.write("<h5 style='color:black;'> Problemática: </h5>", unsafe_allow_html=True)
    st.write("<h8 style='color:black;'> O projeto visa estabelecer através da exposição dos dados um racional lógico das alocações das despesas realizadas pelo Governo de Pernambuco considerando o tempo entre outros atributos presentes no conjunto de dados. </h8>", unsafe_allow_html=True)
   
    st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
 
# 4. CRIANDO UM MENU LATERAL
st.sidebar.image("https://i.postimg.cc/pd2HC7Yy/logo-SENAC-bco.png", width=150)
st.sidebar.image("https://dados.pe.gov.br/uploads/group/2018-03-13-191720.541899brasao.png", width=100)
st.sidebar.image("https://dados.pe.gov.br/uploads/admin/2018-04-12-190707.871446Ati-DadosAbertos-122x55-02.png", width=150)
st.sidebar.header("Filtros")


filtro_ano = st.sidebar.multiselect("Ano", options=df_consolidado['ano'].unique(), default=df_consolidado['ano'].unique())
filtro_modalide_empenho = st.sidebar.multiselect('Modalidade do Empenho', options=df_consolidado['ds_modalidade_empenho'].unique(), default=df_consolidado['ds_modalidade_empenho'].unique())
filtro_unidade_gestora = st.sidebar.multiselect('Unidade Gestora', options=['Todos'] + list(df_consolidado['unidade_gestora'].unique()), default=['Todos'] )
filtro_funcao = st.sidebar.multiselect('Áreas de atuaçăo', options=['Todos'] + list(df_consolidado['cd_nm_funcao'].unique()), default=['Todos'])
filtro_subfuncao = st.sidebar.multiselect('Subáreas de atuaçăo', options=['Todos'] + list(df_consolidado['cd_nm_subfuncao'].unique()), default=['Todos'])


# Equipe
st.sidebar.header("Equipe")
st.sidebar.image("https://i.postimg.cc/C1YQkKL7/Equipe.png", width=200)


# 5 FILTRANDO O DATAFRAME

df_filtrado = df_consolidado

# Aplicando o filtro de ano
if len(filtro_ano) > 0:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(filtro_ano)]

# Aplicando o filtro de modalidade do empenho
if len(filtro_modalide_empenho) > 0:
    df_filtrado = df_filtrado[df_filtrado['ds_modalidade_empenho'].isin(filtro_modalide_empenho)]

# Aplicando o filtro de unidade gestora, ignorando o filtro se 'Todos' estiver selecionado
if 'Todos' not in filtro_unidade_gestora:
    df_filtrado = df_filtrado[df_filtrado['unidade_gestora'].isin(filtro_unidade_gestora)]

# Aplicando o filtro de função (áreas de atuação), ignorando o filtro se 'Todos' estiver selecionado
if 'Todos' not in filtro_funcao:
    df_filtrado = df_filtrado[df_filtrado['cd_nm_funcao'].isin(filtro_funcao)]

# Aplicando o filtro de subfunção (subáreas de atuação), ignorando o filtro se 'Todos' estiver selecionado
if 'Todos' not in filtro_subfuncao:
    df_filtrado = df_filtrado[df_filtrado['cd_nm_subfuncao'].isin(filtro_subfuncao)]


 
# Verificar se a coluna existe "cd_nm_funcao" e tirando os dados NAN
if 'cd_nm_funcao' in df_filtrado.columns:
    # Remover valores nulos antes de contar os valores únicos
    total_secretarias = df_filtrado['cd_nm_funcao'].dropna().nunique()
 
# Verificar se a coluna existe "numero_empenho" e tirando os dados NAN
if 'numero_empenho' in df_filtrado.columns:
    # Remover valores nulos antes de contar os valores únicos
    total_transacoes = df_filtrado['numero_empenho'].dropna().nunique()
 
# Verificar se a coluna existe "credor" e tirando os dados NAN
if 'credor' in df_filtrado.columns:
    # Remover valores nulos antes de contar os valores únicos
    total_fornecedor = df_filtrado['credor'].dropna().nunique()
 
 
# Função para formatar o número de forma compactada
def formatar_valor_compactado(valor):
    if valor >= 1_000_000_000_000:
        return f"R$ {valor/1_000_000_000_000:.2f}T"  # Tilhões
    elif valor >= 1_000_000:
        return f"R$ {valor/1_000_000:.2f}M"  # Tilhões
    elif valor >= 1_000:
        return f"R$ {valor/1_000:.2f}M"  # Bilhões
    else:
        return f"R$ {valor:.2f}"  # Para valores menores que mil
 
# Verificar se a coluna 'vlrtotalpago' existe no DataFrame
if 'vlrtotalpago' in df_filtrado.columns:
    # Somar todos os valores não nulos (ignorando NaN)
    total = df_filtrado['vlrtotalpago'].dropna().sum()
   
    # Formatar o valor de forma compactada
    total_formatado = formatar_valor_compactado(total)
   
 
# Criar colunas
col1, col2, col3, col4 = st.columns(4)
 
# Formatação dos números
col1.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Quantidade de Secretarias</h2>", unsafe_allow_html=True)
col1.markdown(f"<p style='font-size: 50px; color: #1e1e1e'>{(total_secretarias)}</p>", unsafe_allow_html=True)
 
col2.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Quantidade de Transações</h2>", unsafe_allow_html=True)
col2.markdown(f"<p style='font-size: 50px; color: #1e1e1e'>{(total_transacoes)}</p>", unsafe_allow_html=True)
 
col3.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Quantidade de Fornecedores </h2>", unsafe_allow_html=True)
col3.markdown(f"<p style='font-size: 50px; color: #1e1e1e'>{(total_fornecedor)}</p>", unsafe_allow_html=True)
 
col4.markdown(f"<h2 style='font-size: 24px; color: #0958D9;'>Valor Total de Despesas </h2>", unsafe_allow_html=True)
col4.markdown(f"<p style='font-size: 50px; color: #1e1e1e'>{(total_formatado)}</p>", unsafe_allow_html=True)


# 6. ViSUALIZAÇÕES
# INICIO

# 6.1

# Total de despesas por ano (Gráfico de Barras Vertical)
st.write("<h5 style='color:black;'> Total de Despesas por Ano </h5>", unsafe_allow_html=True)
despesas_ano = df_filtrado.groupby('ano')['vlrtotalpago'].sum().reset_index()

fig_area = px.area(
    despesas_ano,
    x="ano",
    y='vlrtotalpago',
    labels={'vlrtotalpago': 'Total de Despesas', 'ano': "Ano"},
    color_discrete_sequence=['#0958D9']
)
# Formatar os valores de 'vlrtotalpago' como strings formatadas
text_labels = despesas_ano['vlrtotalpago'].apply(lambda y: f'R$ {y:,.2f}').tolist()

# Adicionando rótulos diretamente no gráfico de área usando 'mode' adequado
fig_area.update_traces(mode='lines+markers', hovertemplate='R$ %{y:,.2f}', text=text_labels, textposition="top right")

# Configurando o eixo X para mostrar todos os anos
fig_area.update_layout(xaxis=dict(tickmode='linear'))

# Mostrando o gráfico no Streamlit
st.plotly_chart(fig_area)


st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)


# Proporção de proporção da Depesa por Modalidade (Gráfico de Pizza)

st.write("<h5 style='color:black;'> Proporção da Despesal por Modalidade </h5>", unsafe_allow_html=True)

# Calculando a proporção de veículos por tipo
proporcao_veiculos = df_consolidado['ds_modalidade_empenho'].value_counts(normalize=True) * 100
 
# Criando o DataFrame para Plotly
df_proporcao = proporcao_veiculos.reset_index()
df_proporcao.columns = ['ds_modalidade_empenho', 'Proporcao (%)']
 
# Definindo cores
cores = ['#0958D9', '#B0B0B0', '#ffa421']  # Azul padrão, cinza e Laraja
 
# Criando o gráfico de rosca
fig4 = px.pie(
    df_proporcao,
    values='Proporcao (%)',
    names='ds_modalidade_empenho',
    hole=0.5,
    color_discrete_sequence=cores
)
 
# Exibir o gráfico no Streamlit
st.plotly_chart(fig4)

st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# TOP 10 MAIORES DESPESAS POR SECRETARIA
# Exibe um título para a seção no Streamlit com formatação HTML
st.write("<h5 style='color:black;'> Top 10 Secretarias com maiores Despesas </h5>", unsafe_allow_html=True)

# Agrupa o dataframe filtrado, somando o total de despesas por secretaria
secretaria_despesas = df_filtrado.groupby('cd_nm_funcao')['vlrtotalpago'].sum().reset_index()

# Ordena o dataframe pela coluna 'vlrtotalpago' em ordem decrescente (maior para menor)
secretaria_despesas = secretaria_despesas.sort_values('vlrtotalpago', ascending=False).head(10)

# Criar o gráfico de barras horizontais
fig_secretaria_despesas = px.bar(
    secretaria_despesas,
    y='cd_nm_funcao',
    x='vlrtotalpago',
    orientation='h',  # Barras horizontais
    labels={'vlrtotalpago': 'Total de despesas', 'cd_nm_funcao': 'Secretaria'},
    text_auto=True,  # Exibe os valores nas barras
    color_discrete_sequence=['#0958D9']  # Cor personalizada
)

# Atualiza os rótulos dos eixos
fig_secretaria_despesas.update_layout(
    yaxis_title="Secretaria", 
    xaxis_title="Total de despesas",
    yaxis={'categoryorder':'total ascending'}
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig_secretaria_despesas)

st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# TOP 10 MENORES DESPESAS POR SECRETARIA
# Exibe um título para a seção no Streamlit com formatação HTML
st.write("<h5 style='color:black;'> Top 10 Secretarias com menores Despesas </h5>", unsafe_allow_html=True)

# Agrupa o dataframe filtrado, somando o total de despesas por secretaria
secretaria_despesas_menor = df_filtrado.groupby('cd_nm_funcao')['vlrtotalpago'].sum().reset_index()

# Ordena o dataframe pela coluna 'vlrtotalpago' em ordem crescente (menor para maior)
secretaria_despesas_menor = secretaria_despesas_menor.sort_values('vlrtotalpago', ascending=True)

# Seleciona as 10 menores categorias
secretaria_despesas_menor = secretaria_despesas_menor.head(10)

# Criar o gráfico de barras horizontais
fig_secretaria_despesas_menor = px.bar(
    secretaria_despesas_menor,
    y='cd_nm_funcao',
    x='vlrtotalpago',
    orientation='h',  # Barras horizontais
    labels={'vlrtotalpago': 'Total de despesas', 'cd_nm_funcao': 'Secretaria'},
    text_auto=True,  # Exibe os valores nas barras
    color_discrete_sequence=['#0958D9']  # Cor personalizada
)

# Atualiza os rótulos dos eixos
fig_secretaria_despesas_menor.update_layout(
    yaxis_title="Secretaria", 
    xaxis_title="Total de despesas",
    yaxis={'categoryorder':'total descending'}
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig_secretaria_despesas_menor)

st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)


# TOP 10 MAIOR DESPESAS POR AÇÕES
st.write("<h5 style='color:black;'> Top 10 Ações com maiores Despesas </h5>", unsafe_allow_html=True)
acoes_despesas = df_filtrado.groupby('cd_nm_acao')['vlrtotalpago'].sum().reset_index()
acoes_despesas = acoes_despesas.sort_values('vlrtotalpago', ascending=False).head(10)
fig_acoes = px.bar(
    acoes_despesas,
    y='cd_nm_acao',
    x='vlrtotalpago',
    orientation='h',  # Barras horizontais
    labels={'vlrtotalpago': 'Total de despesas', 'cd_nm_acao': 'Ação'},
    text_auto=True,  # Exibe os valores nas barras
    color_discrete_sequence=['#0958D9']  # Cor personalizada
)

fig_acoes.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title="Ação", xaxis_title="Total de despesas")

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig_acoes)


st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# QUANTIDADE DE DESPESAS POR TIPO DE LICITAÇÃO
# Exibe um título para a seção no Streamlit com formatação HTML
st.write("<h5 style='color:black;'> Quantidade de Despesas por tipo de Licitação </h5>", unsafe_allow_html=True)

# Agrupa o dataframe filtrado, contando o número de despesas onde o valor total pago ('vlrtotalpago') é maior que 0
licitacao_despesas = df_filtrado[df_filtrado['vlrtotalpago'] > 0].groupby('ds_tp_licitacao')['vlrtotalpago'].count().reset_index()

# Renomeia a coluna de contagem de despesas para 'contagem'
licitacao_despesas.rename(columns={'vlrtotalpago': 'contagem'}, inplace=True)

# Filtra para manter apenas categorias com contagem maior que 0 e remove entradas nulas
licitacao_despesas = licitacao_despesas[licitacao_despesas['contagem'] > 0].dropna(subset=['contagem'])

# Remove categorias com nome vazio para garantir que apenas dados válidos sejam exibidos
licitacao_despesas = licitacao_despesas[licitacao_despesas['ds_tp_licitacao'] != '']

# Calcula o total de contagem para determinar o percentual
total_contagem = licitacao_despesas['contagem'].sum()

# Calcula o percentual de cada categoria em relação ao total
licitacao_despesas['percentual'] = (licitacao_despesas['contagem'] / total_contagem) * 100

# Cria uma coluna de rótulo que inclui a contagem e o percentual para exibição no gráfico
licitacao_despesas['rotulo'] = licitacao_despesas.apply(lambda row: f"{row['contagem']} ({row['percentual']:.2f}%)", axis=1)

# Ordena o dataframe pela contagem em ordem decrescente
licitacao_despesas = licitacao_despesas.sort_values('contagem', ascending=False)

# Cria um gráfico de barras horizontais usando Plotly Express
fig_licitacao = px.bar(
    licitacao_despesas,  # O dataframe a ser usado
    y='ds_tp_licitacao',  # Eixo Y representando os tipos de licitação
    x='contagem',  # Eixo X representando a contagem de despesas
    orientation='h',  # Define o gráfico como horizontal
    labels={'contagem': 'Contagem de despesas', 'ds_tp_licitacao': 'Tipo Licitação'},  # Rótulos para os eixos
    text=licitacao_despesas['rotulo'],  # Exibe rótulo com contagem e percentual
    color_discrete_sequence=['#43a614']  # Define uma cor personalizada para as barras
)

# Atualiza o layout do gráfico para definir a ordem dos eixos e aumentar a altura
fig_licitacao.update_layout(
    yaxis={'categoryorder':'total ascending'},  # Define a ordem do eixo Y como ascendente
    yaxis_title="Tipo Licitação",  # Título do eixo Y
    xaxis_title="Contagem de despesas",  # Título do eixo X
    height=800  # Aumenta a altura do gráfico para 800 pixels (ajuste conforme necessário)
)

# Exibe o gráfico no Streamlit
st.plotly_chart(fig_licitacao)

st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

 
# Exibir o DataFrame consolidado no Streamlit
st.write("<h5 style='color:black;'> Despesas Consolidadas (2022 - 2024) </h5>", unsafe_allow_html=True)
st.dataframe(df_consolidado.head(100))
st.write("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

