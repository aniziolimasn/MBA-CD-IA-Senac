"""
Aplicação Big Data: Coleta, armazena e exibe cotações de moedas em tempo real.
- Extrai dados de uma API de cotações.
- Armazena no MongoDB Atlas.
- Exibe dashboard interativo com Streamlit.

As variáveis sensíveis de conexão estão em variáveis de ambiente (.env).
"""

import os
import time
import requests
import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis de conexão (NUNCA coloque direto no código!)
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "bancoCotacoes")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cotacoes")

# URL da API de cotações
DATA_URL = "https://economia.awesomeapi.com.br/last/USD-BRLPTAX,EUR-BRLPTAX,BTC-BRL,ETH-BRL,BNB-BRL"

# Conectar ao MongoDB Atlas
def get_database():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[DB_NAME]

db = get_database()
collection = db[COLLECTION_NAME]

# Função para buscar e armazenar dados da API no MongoDB
def fetch_and_store_data():
    try:
        response = requests.get(DATA_URL)
        if response.status_code == 200:
            data = response.json()
            dt_extracao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filtered_data = []
            for key, value in data.items():
                filtered_data.append({
                    "code": value["code"],
                    "codein": value["codein"],
                    "name": value["name"],
                    "bid": float(value["bid"]),
                    "ask": float(value["ask"]),
                    "timestamp": int(value["timestamp"]),
                    "create_date": value["create_date"],
                    "dt_extracao": dt_extracao
                })
            # Inserir dados no MongoDB
            document = {
                "timestamp": time.time(),
                "cotacoes": filtered_data
            }
            collection.insert_one(document)
        else:
            print(f"Erro ao buscar os dados: {response.status_code}")
    except Exception as e:
        print("Erro na requisição ou inserção no MongoDB:", str(e))

# Função para buscar todos os dados do MongoDB
def fetch_all_data():
    try:
        all_documents = collection.find()
        all_cotacoes = []
        for doc in all_documents:
            all_cotacoes.extend(doc.get("cotacoes", []))
        df = pd.DataFrame(all_cotacoes)
        if not df.empty:
            df["dt_extracao"] = pd.to_datetime(df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")
        return df
    except Exception as e:
        st.error(f"Erro ao recuperar os dados do MongoDB: {str(e)}")
        return None

# Função para buscar o último registro do MongoDB
def fetch_last_data():
    try:
        last_document = collection.find_one(sort=[("_id", -1)])
        if not last_document or "cotacoes" not in last_document:
            return None
        df = pd.DataFrame(last_document["cotacoes"])
        if not df.empty:
            df["dt_extracao"] = pd.to_datetime(df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")
        return df
    except Exception as e:
        st.error(f"Erro ao recuperar os dados do MongoDB: {str(e)}")
        return None

# ===================== DASHBOARD STREAMLIT =====================

# Configurar a tela em formato wide
st.set_page_config(layout="wide")

# Buscar último registro para o scroller
last = fetch_last_data()
if last is not None and not last.empty:
    moedas = [tuple(row) for row in last[['code', 'bid']].values]
    espaco = "    "
    texto_base = espaco.join(
        [f"{moeda}: <span style='color: #02E201; font-weight: bold;'>R${valor:,.2f}</span>" for moeda, valor in moedas]
    )
else:
    texto_base = "Sem dados disponíveis"

def get_last_updated():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

# CSS do scroller
css = """
<style>
.title { font-size: 32px !important; font-weight: bold; text-align: center; margin-bottom: 20px; }
.scroller-container { width: 60%; overflow: hidden; white-space: nowrap; margin: auto; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);}
.scroller-text { font-size: 24px !important; font-weight: bold; font-family: Arial, sans-serif; display: inline-block; animation: scrollText 15s linear infinite;}
.update-time { font-size: 18px; font-weight: bold; color: #555; margin: 10px 0;}
@keyframes scrollText { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Container do scroller
container_style = f"""
<div style="width: 60%; margin: auto; text-align: center;">
    <img src="https://i.postimg.cc/tTc29F0x/Capa.png" width="1200">
    <div>---</div>
    <div>
        Frequência atualizações: 
        <span style="color:#02E201;">API - Tempo real</span> | 
        <span style="color:#02E201;">MongoDb Atlas - 60 segundos</span> | 
        <span style="color:#02E201;">Streamlit - 30 segundos</span>
    </div>
    <div class="update-time">Última atualização dashboard: {get_last_updated()}</div>
    <div>---</div>
    <div class="scroller-container">
        <p class="scroller-text">{texto_base}</p>
    </div>
</div>
"""
st.markdown(container_style, unsafe_allow_html=True)

# Buscar todos os dados para o dashboard
df = fetch_all_data()

if df is not None and not df.empty:
    df['ask'] = pd.to_numeric(df['ask'], errors='coerce')
    df['bid'] = pd.to_numeric(df['bid'], errors='coerce')
    df['dt_extracao'] = pd.to_datetime(df['dt_extracao'], errors='coerce')
    available_currencies = df['name'].unique().tolist()

    # Seletor de moeda
    st.markdown(
        """<div style="width: 50%; margin: auto; text-align: left; padding: 10px;">
        <p style="font-size: 18px; color: gray;font-weight: bold;"> Selecione a moeda:</p>
        </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_currency = st.selectbox("", available_currencies, key="moeda")

    # Título "Última Cotação"
    st.markdown(
        """<div style="width: 50%; margin: auto; text-align: left; padding: 10px;">
        <p style="font-size: 18px; color: gray;font-weight: bold;">Última Cotação da Moeda Selecionada</p>
        </div>""", unsafe_allow_html=True)

    # Filtrar dados para a moeda selecionada
    df_currency = df[df['name'] == selected_currency].sort_values(by='dt_extracao', ascending=False)
    df_currency_last_50 = df_currency.head(50)
    last_record = df_currency_last_50.iloc[0]

    # Exibir última cotação
    st.markdown(
        f"""<div style="width: 50%; margin: auto; text-align: left; border: 2px solid gray; padding: 10px; border-radius: 10px;">
        <p style="font-size: 18px; font-weight: bold; color: #fffff;">💰 Preço de Compra: <span style="font-size: 20px; font-weight: bold; color: #02E201;">{last_record['bid']}</span></p>
        <p style="font-size: 18px; font-weight: bold; color: #fffff;">💲 Preço de Venda: <span style="font-size: 20px; font-weight: bold; color: #02E201;">{last_record['ask']}</span></p>
        <p style="font-size: 18px; font-weight: bold; color: #fffff;">📅 Última Atualização: <span style="font-size: 20px; font-weight: bold; color: #02E201;">{last_record['dt_extracao']}</span></p>
        </div>""", unsafe_allow_html=True)

    # Gráfico de linha
    df_fig = df_currency[['bid', 'ask', 'dt_extracao']]
    df_fig['dt_extracao'] = pd.to_datetime(df_fig['dt_extracao'], errors='coerce')
    df_fig.set_index('dt_extracao', inplace=True)
    df_fig_resample = df_fig.resample('60T').mean().dropna().reset_index()
    df_fig_resample['compra'] = df_fig_resample['bid']
    df_fig_resample['venda'] = df_fig_resample['ask']

    # Botões para escolha entre compra/venda
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
    with col2:
        compra_button = st.button("Compra", use_container_width=True)
    with col3:
        venda_button = st.button("Venda", use_container_width=True)
    display_choice = "compra"
    if compra_button:
        display_choice = "compra"
    elif venda_button:
        display_choice = "venda"
    min_val = df_fig_resample[display_choice].min()
    max_val = df_fig_resample[display_choice].max()
    min_limit = min_val * 0.9
    max_limit = max_val * 1.1

    # Gráfico Altair
    line_chart = alt.Chart(df_fig_resample).mark_line(strokeWidth=2).encode(
        x=alt.X('dt_extracao:T', axis=alt.Axis(title=None)),
        y=alt.Y(f'{display_choice}:Q', axis=alt.Axis(title=None), scale=alt.Scale(domain=[min_limit, max_limit])),
        color=alt.value("#02E201" if display_choice == "compra" else "#FE0560")
    )
    point_chart = alt.Chart(df_fig_resample).mark_circle(size=50).encode(
        x='dt_extracao:T',
        y=f'{display_choice}:Q',
        color=alt.value("#02E201" if display_choice == "compra" else "#FE0560")
    )
    chart = (line_chart + point_chart).properties(width=800, height=400)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(chart, use_container_width=True)
else:
    st.warning("⚠️ Nenhum dado encontrado no banco!")

# Atualização automática da página
update_interval = 30
st.query_params["refresh_time"] = int(time.time())
time.sleep(update_interval)
st.rerun()