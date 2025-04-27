# Projeto Grupo 3 - Análise de Vendas Walmart
# Autor: Anizio Neto
# Data: 02/05/2024
# Objetivo: Realizar uma análise exploratória dos dados de vendas do Walmart, incluindo tratamento de datas, cálculo de estatísticas e geração de gráficos.
# Descrição: Este script realiza análise exploratória dos dados de vendas do Walmart, incluindo tratamento de datas, cálculo de estatísticas e geração de gráficos.

############### IMPORTAÇÃO DOS DADOS ###############
# Lê o arquivo CSV contendo os dados de vendas
# O arquivo CSV deve estar no mesmo diretório deste script R
base_path <- getwd() # Obtém o diretório atual de trabalho
csv_file <- file.path(base_path, "Grupo 3 - Vendas - Walmart.csv")
dados <- read.csv(csv_file, sep=",", header = TRUE)

############### IMPORTAÇÃO E CARREGAMENTO DE BIBLIOTECAS ###############
# Instale os pacotes apenas se necessário (recomenda-se rodar manualmente se já estiverem instalados)
# install.packages("lubridate") # Para manipulação de datas
# install.packages("ggcorrplot") # Para gráficos de correlação

library(lubridate)   # Manipulação de datas
library(ggcorrplot)  # Gráficos de correlação

############### TRATAMENTO DE DATAS ###############
# Converte a coluna 'Data' para o formato Date
# Formato esperado: dia-mês-ano (ex: 01-01-2020)
dados$data_convertida <- as.Date(dados$Data, format = "%d-%m-%Y")

############### CRIAÇÃO DE COLUNAS TEMPORAIS DERIVADAS ###############
# Extrai informações temporais úteis para análise

dados$ano <-  year(dados$data_convertida)           # Ano
dados$mes <- month(dados$data_convertida)           # Mês
dados$dia <- day(dados$data_convertida)             # Dia do mês
dados$dia_semana <- weekdays(dados$data_convertida) # Dia da semana
dados$dia_ano <- yday(dados$data_convertida)        # Dia do ano
dados$num_semana_ano <- week(dados$data_convertida) # Número da semana no ano
dados$trimestre <- quarter(dados$data_convertida)   # Trimestre
dados$AnoTrimestre <- (dados$ano*100)+dados$trimestre # Identificador único ano+trimestre

############### PRINCIPAIS MEDIDAS ESTATÍSTICAS ###############
# Calcula médias das principais variáveis numéricas

vMediaVendaSemana <- mean(dados$VendaSemana)
vMediaTemperaturaF <- mean(dados$Temperatura)
vMediaCustoCombustivel <- mean(dados$CustoCombustivel)
vMediaTaxaDesemprego <- mean(dados$TaxaDesemprego)

# Exibe as médias calculadas
cat("Média de Vendas por Semana:", vMediaVendaSemana, "\n")
cat("Média de Temperatura:", vMediaTemperaturaF, "\n")
cat("Média de Custo do Combustível:", vMediaCustoCombustivel, "\n")
cat("Média de Taxa de Desemprego:", vMediaTaxaDesemprego, "\n")

############### GERAÇÃO DE GRÁFICOS EXPLORATÓRIOS ###############

# Gráfico de barras: Média de vendas por loja
barplot(
  tapply(dados$VendaSemana, dados$Loja, mean),
  main = "Média de Vendas por Loja",
  xlab = "Loja",
  ylab = "Média de Vendas",
  col = 3
)

# Gráfico de barras: Média de vendas por mês
barplot(
  tapply(dados$VendaSemana, dados$mes, mean),
  main = "Média de Vendas por Mês",
  xlab = "Mês",
  ylab = "Média de Vendas",
  col = 3
)

# Gráfico de barras: Média de vendas por ano
barplot(
  tapply(dados$VendaSemana, dados$ano, mean),
  main = "Média de Vendas por Ano",
  xlab = "Ano",
  ylab = "Média de Vendas",
  col = 3
)

# Gráfico de barras horizontal: Representatividade percentual das vendas por loja
barplot(
  sort(100 * tapply(dados$VendaSemana, dados$Loja, sum) / sum(dados$VendaSemana), decreasing = FALSE),
  main = "Representatividade de Vendas por Loja",
  xlab = "Percentual do Total de Vendas",
  ylab = "Loja",
  col = 3,
  horiz = TRUE
)

# Data frame com médias mensais de poder de compra e taxa de desemprego
d <- data.frame(
  MediaPoderCompra = tapply(dados$PoderCompra, dados$mes, mean),
  MediaTaxaDesemprego = tapply(dados$TaxaDesemprego, dados$mes, mean)
)

# Matriz de correlação e gráfico de correlação entre poder de compra e taxa de desemprego
cor <- cor(d)
ggcorrplot(cor, hc.order = TRUE, type = "lower", lab = TRUE)

# Gráfico de dispersão: Poder de compra vs Taxa de desemprego
plot(
  d$MediaTaxaDesemprego, d$MediaPoderCompra,
  main = "Correlação Poder de Compra vs Taxa de Desemprego",
  xlab = "Média mês Taxa Desemprego",
  ylab = "Média mês Poder de Compra",
  pch = 16,
  col = 3
)

# Boxplot: Vendas por ano
boxplot(
  dados$VendaSemana ~ dados$ano,
  main = "Vendas por Ano",
  xlab = "Ano",
  ylab = "Vendas Semanais",
  col = c(4,5,6)
)

# Boxplot: Custo do combustível por ano
boxplot(
  dados$CustoCombustivel ~ dados$ano,
  main = "Combustível por Ano",
  xlab = "Ano",
  ylab = "Custo do Combustível",
  col = c(4,5,6)
)

# Boxplot: Taxa de desemprego por ano
boxplot(
  dados$TaxaDesemprego ~ dados$ano,
  main = "Taxa de Desemprego por Ano",
  xlab = "Ano",
  ylab = "Taxa de Desemprego",
  col = c(4,5,6)
)

# Fim do script


