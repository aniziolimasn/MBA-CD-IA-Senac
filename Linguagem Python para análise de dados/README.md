# LEIAME - Dashboard de Análise de Sinistros de Trânsito

## Finalidade
Este projeto implementa um dashboard interativo em Python/Streamlit para análise de acidentes de trânsito na cidade do Recife, utilizando dados históricos da CTTU (2016-2024).

## Funcionalidades
- Unificação automática de arquivos CSV anuais de acidentes.
- Filtros interativos por tipo de acidente e intervalo de datas.
- Visualizações: totais, gráficos por ano, mês, bairro, mapa de calor.
- Recomendação de rotas seguras baseada em classificação de risco por bairro (Machine Learning).

## Como usar
1. Coloque todos os arquivos acidentes*.csv na mesma pasta do script.
2. Execute o script com:
   ```
   streamlit run dash_cttu_novo.py
   ```
3. Utilize os filtros e explore as visualizações.

## Requisitos
- Python 3.8+
- Veja o arquivo requirements.txt para dependências.

## Autor
Faculdade SENAC - PE / MBA Ciência de Dados e IA / Prof. Geraldo Gomes / Agosto 2024
