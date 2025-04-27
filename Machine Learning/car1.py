"""
Finalidade do Código:
---------------------
Este script realiza um pipeline completo de Machine Learning para previsão de preços de veículos, utilizando dados históricos e variáveis relevantes do mercado automotivo. O objetivo é criar uma ferramenta interativa, baseada em Python e Streamlit, que permita ao usuário simular cenários, analisar fatores que influenciam o valor dos veículos e obter recomendações de preço personalizadas. O código abrange desde a extração, limpeza e pré-processamento dos dados, até o treinamento, avaliação e comparação de diferentes modelos de regressão, além da visualização dos resultados e interação dinâmica com o usuário.
"""

####################################### 0. IMPORTAÇÕES DAS BIBLIOTECAS ##########################################

# Importação das bibliotecas essenciais para análise de dados, visualização e machine learning
import pandas as pd  # Manipulação de dados em DataFrames
import numpy as np  # Operações numéricas e tratamento de valores nulos
import matplotlib.pyplot as plt  # Visualização de gráficos
import streamlit as st  # Criação de dashboards interativos
import seaborn as sns  # Visualização estatística avançada

# Importação dos modelos de Machine Learning e utilitários do scikit-learn
from sklearn.ensemble import RandomForestRegressor # Modelo 1: Regressão por Floresta Aleatória
from sklearn.linear_model import LinearRegression # Modelo 2: Regressão Linear
from sklearn.tree import DecisionTreeRegressor # Modelo 3: Árvore de Decisão
from sklearn.impute import SimpleImputer  # Tratamento de valores ausentes
from sklearn.preprocessing import OneHotEncoder  # Codificação de variáveis categóricas
from sklearn.model_selection import train_test_split, cross_val_score  # Divisão e validação dos dados
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, mean_squared_error, r2_score  # Métricas de avaliação
from sklearn.compose import ColumnTransformer  # Pré-processamento de colunas

###################################### 1. EXTRAÇÃO E CARREGAMENTO DOS DADOS ######################################

# Leitura do arquivo CSV contendo os dados dos veículos
# O caminho do arquivo deve ser ajustado conforme o local onde está salvo
file_path = "car_price_prediction.csv"
data = pd.read_csv(file_path)

###################################### 2. TRATAMENTO DE VALORES NULOS E VAZIOS ###################################

# Exclusão de colunas consideradas irrelevantes para a análise e predição de preço
columns_to_drop = [
    "Leather interior", "Wheel", "Color", "ID"
]
data.drop(columns=columns_to_drop, inplace=True)

# Renomeando colunas para o português, facilitando a leitura e entendimento
# Exemplo: 'Engine volume' -> 'Tamanho do Motor'
data.rename(
    columns={
        "Engine volume": "Tamanho do Motor",
        "Price": "Preço",
        "Manufacturer": "Fabricante",
        "Model": "Modelo",
        "Prod. year": "Ano",
        "Category": "Categoria",
        "Fuel type": "Tipo de Combustível",
        "Mileage": "Quilometragem",
        "Gear box type": "Tipo de Câmbio",
        "Drive wheels": "Tração",
        "Levy": "Imposto",
        'Cylinders': "Cilindros",
        "Doors": "Portas"
    },
    inplace=True,
)

# Limpeza e conversão dos dados para os tipos corretos
# Remove a palavra 'Turbo' e converte para numérico
# Limpeza e conversão da coluna "Tamanho do Motor"
data['Tamanho do Motor']=data['Tamanho do Motor'].str.replace('Turbo','')
data['Tamanho do Motor']=pd.to_numeric(data['Tamanho do Motor'])

# Limpeza e conversão da coluna "Quilometragem" (remove 'km' e converte para número)
data['Quilometragem']=data['Quilometragem'].str.replace('km',"")
data['Quilometragem']=pd.to_numeric(data['Quilometragem'])

# Limpeza e conversão da coluna "Imposto" (substitui '-' por NaN e converte para número)
data["Imposto"] = data["Imposto"].astype(str).replace("-", np.nan)
data["Imposto"] = pd.to_numeric(data["Imposto"], errors="coerce")

# Limpeza e conversão da coluna "Portas" (corrige valores inconsistentes)
data['Portas'].replace({'04-May':4, '02-Mar':2, '>5':5}, inplace=True)
    

# Função para tratamento de valores nulos
# Substitui valores nulos em colunas numéricas pela mediana e em categóricas por 'DESCONHECIDO'
def handle_missing_values(df):
    # Para dados numéricos: substitui valores nulos pela mediana
    numeric_columns = ["Preço", "Imposto", "Quilometragem", 'Tamanho do Motor', 'Cilindros']
    imputer_numeric = SimpleImputer(strategy="median")
    df[numeric_columns] = imputer_numeric.fit_transform(df[numeric_columns])

    # Para dados categóricos: substitui valores nulos por "DESCONHECIDO"
    categorical_columns = [
        "Fabricante", "Modelo", "Categoria", "Tipo de Combustível", 
        "Tipo de Câmbio", "Tração"
    ]
    for col in categorical_columns:
        df[col] = df[col].fillna("DESCONHECIDO").str.strip().str.upper()
    
    return df

# Aplica o tratamento de valores nulos ao DataFrame principal
data = handle_missing_values(data)

df_tratado = data  # Mantém uma cópia dos dados tratados para uso posterior

# Lista de colunas numéricas para referência
numeric_columns = ['Preço','Imposto','Quilometragem','Ano', 'Tamanho do Motor', 'Cilindros', 'Airbags']


###################################### 3. TRANSFORMAÇÃO E PRÉ-PROCESSAMENTO ######################################

# Codificação One-Hot para colunas categóricas
encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
categorical_columns = [
    "Fabricante", "Modelo", "Categoria", "Tipo de Combustível", 
    "Tipo de Câmbio", "Tração"
]
encoded_features = encoder.fit_transform(data[categorical_columns])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_columns))

# Combinar dados numéricos e codificados
data = pd.concat([data.drop(columns=categorical_columns), encoded_df], axis=1)

# Definir X (variáveis independentes) e y (variável dependente)
X = data.drop(columns=["Preço"])  
y = data["Preço"]

###################################### 4. DIVISÃO EM TREINO E TESTE ######################################

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

###################################### 5. TREINAMENTO DOS MODELOS ######################################

# Configuração dos modelos
models = {
    "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=10)
}

# Resultados dos modelos
results = {}
for model_name, model in models.items():
    # Treinar o modelo
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred = model.predict(X_test)
    
    # Avaliação
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Validação cruzada
    cv_scores = cross_val_score(model, X, y, cv=5, n_jobs=-1)
    mean_cv_score = np.mean(cv_scores)
    
    # Adicionar resultados ao dicionário
    results[model_name] = {
         "MSE": mse,
         "R²": r2,
         "CV Mean Score": mean_cv_score,
    }

# Selecionar o melhor modelo baseado no R²
if results:  # Verificar se existem resultados
    best_model = max(results, key=lambda x: results[x]["R²"])
else:
    raise ValueError("Nenhum modelo foi avaliado corretamente. Verifique os dados de entrada e a configuração dos modelos.")

###################################### Treimanento do Melhor Modelo #########################
x_model_1 = df_tratado.drop(columns=['Preço'])
y_model_1 = df_tratado['Preço']

categorical_features = x_model_1.select_dtypes(include=['object']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', X.select_dtypes(exclude=['object']).columns)
    ])

# Dividindo os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_1 = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
model_1.fit(X_train,y_train)

y_pred_m1 = model_1.predict(X_test)


##################################### 6. DATA VISUALIZATION - STREAMLIT ######################################

# Título com imagem de fundo
st.image("https://i.postimg.cc/fb5kX3SS/Banner-car-price.png")

st.write("---")

st.write("<h4 style='color:white; font-size:20px;'> Faculdade SENAC/ PE - MBA Ciência de Dados e Inteligência Artificial </h4>", unsafe_allow_html=True)
st.write("<h4 style='color:white; font-size:15px;'> Projeto Final Disciplina Machine Learning (Prof. Geraldo Gomes) * Dezembro 2024 </h4>", unsafe_allow_html=True)

st.write("---")

# Exibição de equipe e descrição
st.write("### Equipe")
st.image("https://i.postimg.cc/BnMN8NDN/Equipe.png", width=700)

st.write("---")

# Storytelling
st.write("### Storytelling")
st.write("Data Explorer")
st.write("Dados:")
st.write("""<h7 style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Base: <span style="color:#4894CA; font-weight:semibold;">car_price_prediction.csv</span> | 
    Fonte Kaggle: <a href='https://www.kaggle.com/datasets/deepcontractor/car-price-prediction-challenge' target='_blank' style="color:#4894CA; text-decoration:none;"> Clique aqui</a></h7> """, unsafe_allow_html=True)
st.write("""<h7 style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Ideal Para: <span style="color:#4894CA;"> Regressão em dados relacionados a veículos</span> </h7>""", unsafe_allow_html=True)

st.write(f"""<h5 style='color:yellow; font-size:15px;'> Ponto de melhoria: Realizar extração direta no Kaggle (via web), como forma de melhorar a performance do modelo. </h5>""", unsafe_allow_html=True)

st.write("Analise:")
st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Tema: <span style="color:#4894CA;"> Previsão de preços de veículos com base em dados históricos e variáveis relevantes</span></div>""", unsafe_allow_html=True)
st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Argumento: <span style="color:#4894CA;"> Modelos de regressão podem ajudar empresas a entender os fatores que influenciam o valor de um veículo, promovendo estratégias de precificação mais precisas e competitivas.</span></div>""", unsafe_allow_html=True)

st.write("Story Construction")
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Informações: <span style="color:#4894CA;"> A base de dados contém características como marca, modelo, ano, quilometragem e outras variáveis que afetam o preço do veículo.</span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Insights: <span style="color:#4894CA;"> Variáveis como quilometragem e ano de fabricação têm forte influência no preço. Modelos específicos apresentam depreciação mais acentuada.</span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Personagens: <span style="color:#4894CA;"> Empresários do ramo automobilístico, gestores de frotas, consumidores e pesquisadores do mercado automotivo.</span></div>""", unsafe_allow_html=True)

st.write("Story Apresentation")
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Público-Alvo: <span style="color:#4894CA;"> Empresários do ramo automobilístico, frotistas, integrantes do governo </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Objetivo: <span style="color:#4894CA;"> Estimar o preço de veículos com base em variáveis </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Apresentação: <span style="color:#4894CA;"> Será realizada de forma presencial ou remota, utilizando a ferramenta Teams, bem como a IDE VsCode, fazendo uso das linguagens Python e HTML através da biblioteca “Streamlit” para demonstração da ferramenta confeccionada para aplicação do conhecimento adiquirido na disciplina de Machine Learning.</span></div>""", unsafe_allow_html=True)


st.write("---")

st.write("### Tratamento e Análise")

st.write(f"""<h5 style='color:white; font-size:15px;'> Com o intuito de obter as melhores análises possíveis, temos que fornecer a melhor qualidade dos nossos dados, por isso foi feito algumas exclusões de coluna que julgamos não ser do interesse tanto da nossa análise quando impactam no modelo:</h5>""", unsafe_allow_html=True)

st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> "Leather interior": <span style="color:#4894CA;">
Traduzida como "Interior em couro", diz respeito a customização interna do veículo, algo que foge da nossa análise.
</span></div>""", unsafe_allow_html=True)

st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> "Wheel": <span style="color:#4894CA;">
Traduzido como "Roda", como todos os carros possuem 4 rodas, não tem a necessidade de ter essa coluna no nosso Data Frame.
</span></div>""", unsafe_allow_html=True)

st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'>  "Color": <span style="color:#4894CA;">
Traduzido como "Cor", sendo a cor do veículo. Na nossa análise não colocamos essa Coluna para influenciar no resultado, pois julgamos que não tenha um impactos na predição de Preço
</span></div>""", unsafe_allow_html=True)

st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'>  "ID": <span style="color:#4894CA;">
Coluna de ID que pode ser facilmente descartada para otimizar o desempenho do DataFrame.
</span></div>""", unsafe_allow_html=True)

st.write(f"""<h5 style='color:yellow; font-size:15px;'> Ponto de melhoria: Fundamentar o "Drop" de colunas com base na análise de correlação dos dados, depois exibir em gráfico. </h5>""", unsafe_allow_html=True)


st.write("---")

st.write("### Modelagem e Avaliação")

st.write(f"""<h5 style='color:white; font-size:15px;'> Objetivo do modelo: Fornecer previsões precisas e personalizadas de preços, com base no cenário simulado pelo usuário utilizando filtros, a seguir, que representarão as principais variáveis do modelo (features).</h5>""", unsafe_allow_html=True)

# Justificativa de escolha dos modelos
st.write("Por que escolhemos os modelos supervisionados abaixo:")
st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Random Forest: <span style="color:#4894CA;">
Um modelo poderoso para problemas de regressão, como a previsão de preços de carros, pois consegue capturar interações não-lineares entre variáveis. Sua capacidade de lidar com dados categóricos (como marcas e tipos de combustível) e numéricos (como quilometragem e preço) o torna uma escolha robusta para esse tipo de análise.
</span></div>""", unsafe_allow_html=True)
st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Linear Regression: <span style="color:#4894CA;">
Ideal para identificar tendências lineares nos dados, como a relação inversa entre a quilometragem de um carro e seu preço. Além disso, fornece interpretabilidade, ajudando a entender a contribuição de variáveis individuais no preço final do carro.
</span></div>""", unsafe_allow_html=True)
st.write("""<div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'>Decision Tree: <span style="color:#4894CA;">
É útil para criar regras de decisão claras, como "se a idade do carro for maior que 5 anos e a quilometragem acima de 100.000 km, o preço será reduzido em média X%". Essas regras tornam o modelo interpretável para analisar como os preços dos carros são determinados com base nas características.
</span></div>""", unsafe_allow_html=True)

# Convertendo os resultados para um DataFrame para exibição
results_df = pd.DataFrame(results).T  
results_df['Cross Validation Mean'] = mean_cv_score
results_df = results_df.round({'MSE': 2, 'R²': 2, 'Cross Validation Mean': 2})

# Exibir a tabela de resultados
st.write("""<h4 style='color:white; font-size:15px;'> Resultados de <span style="color:#4894CA;">MSE</span>, <span style="color:#4894CA;">R²</span> e <span style="color:#4894CA;">Cross Validation</span>:</h4>""", unsafe_allow_html=True)
st.dataframe(results_df)

# Exibir o nome do melhor modelo
st.write(f"""<h4 style='color:white; font-size:15px;'> Melhor modelo: </span><span style='color:#4894CA;'>{best_model}</span></h4>""", unsafe_allow_html=True)

# Adicão de notas
st.write("Notas:")
st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> MSE (Mean Squared Error):<span style="color:#4894CA;"> Métrica utilizada para medir a qualidade de um modelo de regressão. Ele calcula a média dos quadrados dos erros, ou seja, a diferença entre os valores previstos pelo modelo e os valores reais (observados). </span></div>""", unsafe_allow_html=True)

st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> O Random Forest apresentou o menor MSE, indicando que suas previsões foram as mais próximas dos valores reais. Isso reflete sua capacidade de capturar interações complexas entre variáveis categóricas e numéricas, como marcas e quilometragem. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> Modelos como Linear Regression tendem a apresentar maiores MSEs quando a relação entre as variáveis é não-linear ou há múltiplas interações que não podem ser representadas por uma única equação linear. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Interpretação: Um menor MSE significa que o modelo é adequado para fornecer previsões personalizadas e precisas, alinhando-se ao objetivo de prever preços de forma robusta.</span></div>""", unsafe_allow_html=True)


st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> R² (Coeficiente de Determinação): <span style="color:#4894CA;"> Mede quão bem o modelo de regressão se ajusta aos dados. Indica a proporção da variabilidade dos dados que é explicada pelo modelo. O R² varia de 0 a 1, sendo que valores mais próximos de 1 indicam um melhor ajuste do modelo. </span></div>""", unsafe_allow_html=True)

st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> O Random Forest apresentou o maior R² entre os modelos, indicando que ele explica a maior parte da variação nos preços dos carros, capturando os padrões dos dados com maior eficiência. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> O Decision Tree, apesar de ser mais interpretável, pode ter um R² inferior devido à tendência de overfitting ou à simplicidade da modelagem em comparação com o Random Forest. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> A Linear Regression, por outro lado, pode ter dificuldades em ajustar adequadamente padrões não-lineares, resultando em um R² menor. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Interpretação: Um R² mais alto reforça que o Random Forest é o modelo mais indicado para capturar a relação entre variáveis preditoras e o preço, atendendo ao objetivo de fornecer previsões baseadas em filtros simulados pelo usuário. </span></div>""", unsafe_allow_html=True)

st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Validação cruzada: <span style="color:#4894CA;"> A adição da validação cruzada elimina vieses e aumenta a robustez das avaliações. </span></div>""", unsafe_allow_html=True)

st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> O uso de validação cruzada garantiu que os resultados não fossem enviesados ou específicos de um subconjunto de dados, permitindo avaliar os modelos em um contexto mais amplo. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> Para o Random Forest, a validação cruzada reforça sua robustez e a consistência nos resultados, apesar do maior custo computacional. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:30px; margin-bottom:10px;'> O Linear Regression e o Decision Tree podem ter apresentado maior variabilidade entre as divisões, destacando fragilidades na generalização. </span></div>""", unsafe_allow_html=True)
st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Interpretação: A validação cruzada valida o desempenho superior do Random Forest em termos de precisão e capacidade de generalização. </span></div>""", unsafe_allow_html=True)

st.write(""" <div style='color:white; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Custos computacionais: <span style="color:#4894CA;"> Os custos computacionais podem aumentar o tempo de execução, mas o uso de n_jobs=-1 paraleliza os cálculos para mitigar esse impacto. </span></div>""", unsafe_allow_html=True)

st.write("---")

# Modelos disponíveis
models = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42)  # Adicionando o Decision Tree
}

############################### VERIFICAR O DESEMPENHO ##################################################################################################################################

# Streamlit - SelectBox para escolher o modelo
st.write("Desempenho:")
model_choice = st.selectbox("Escolha o modelo", options=list(models.keys()))

# Treinamento do modelo selecionado
model = models[model_choice]
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Gráfico desempenho do modelo
plt.figure(figsize=(8, 6), facecolor='#0F1117')
ax = plt.gca()  
ax.set_facecolor('#0F1117')  
ax.tick_params(axis='both', colors='white')  
ax.spines['top'].set_color('white')  
ax.spines['right'].set_color('white') 
ax.spines['left'].set_color('white')  
ax.spines['bottom'].set_color('white') 

# Plotando os pontos
plt.scatter(y_test, y_pred, alpha=0.6, color="#4894CA")
plt.scatter(y_test, y_test, alpha=0.6, color="#FFA500")

# Ajustando a cor do texto (branco)
plt.xlabel("Valores Reais", color="#FFA500")
plt.ylabel("Valores Previstos", color="#4894CA")

# Exibindo o gráfico no Streamlit
st.pyplot(plt)

st.write("Nota:")
st.write(""" <div style='color:gray; font-size:14px; font-family:Arial, sans-serif; margin-left:20px; margin-bottom:10px;'> Finalidade: <span style="color:#4894CA;"> O gráfico acima visa demonstrar dinâmicamente o desempenho dos diferentes tipos de modelo abordados no projeto. </span></div>""", unsafe_allow_html=True)

st.write("---")

# DataFrame com a logo marca dos fabricantes - URLs
data_marca = {
    "fabricante": [
        "ACURA", "ALFA ROMEO", "ASTON MARTIN", "AUDI", "BENTLEY", "BMW", "BUICK", "CADILLAC", "CHEVROLET", "CHRYSLER",
        "DAEWOO", "DAIHATSU", "DODGE", "FERRARI", "FIAT", "FORD", "GAZ", "GMC", "GREATWALL", "HAVAL", "HONDA", "HUMMER",
        "HYUNDAI", "INFINITI", "ISUZU", "JAGUAR", "JEEP", "KIA", "LAMBORGHINI", "LANCIA", "LAND ROVER", "LEXUS", "LINCOLN",
        "MASERATI", "MAZDA", "MERCEDES-BENZ", "MERCURY", "MINI", "MITSUBISHI", "MOSKVICH", "NISSAN", "OPEL", "PEUGEOT",
        "PONTIAC", "PORSCHE", "RENAULT", "ROLLS-ROYCE", "ROVER", "SAAB","SCION","SEAT","SKODA","SSANGYONG","SUBARU","SUZUKI",
        "TESLA","TOYOTA","UAZ","VAZ","VOLKSWAGEN","VOLVO","ZAZ" 
    ],
    "logo": [
        "https://i.postimg.cc/RZY6jSJ2/acura.png",
        "https://i.postimg.cc/d3nDnwKH/alfa-romeu.png",
        "https://i.postimg.cc/mZScTNFY/aston-martin.png",
        "https://i.postimg.cc/RhvNcq2J/audi.png",
        "https://i.postimg.cc/T3T1FyPk/R.png",
        "https://i.postimg.cc/KYgkb6nj/bmw.png",
        "https://i.postimg.cc/MT2cp9DD/buick.png",
        "https://i.postimg.cc/k4Q26WYd/cadilac.png",
        "https://logos-world.net/wp-content/uploads/2021/03/Chevrolet-Logo.png",
        "https://i.postimg.cc/nc0QGYFF/chrysler.png",
        "https://i.postimg.cc/SKzFF9YY/daewoo.png",
        "https://i.postimg.cc/PfbH513m/daihatsu.png",
        "https://i.postimg.cc/LXXP8HRP/dodge.png",
        "https://i.postimg.cc/zBtnCypp/ferrari.png",
        "https://i.postimg.cc/C1j3dVNF/fiat.png",
        "https://i.postimg.cc/Y0PzHvWj/ford.png",
        "https://i.postimg.cc/TPvQ15HD/gaz.png",
        "https://i.postimg.cc/wjr8G2Md/gmc.png",
        "https://i.postimg.cc/h4Zrx55g/greatwall.png",
        "https://i.postimg.cc/Jn1qcV87/haval.png",
        "https://i.postimg.cc/VLNhPt3s/honda.png",
        "https://i.postimg.cc/tC7BMjxY/hummer.png",
        "https://i.postimg.cc/gJF9Y03S/huyndai.png",
        "https://i.postimg.cc/7YBp59gT/infiniti.png",
        "https://i.postimg.cc/2j0HG63s/isuzu.png",
        "https://i.postimg.cc/dVppB0Ns/jaguar.png",
        "https://i.postimg.cc/fWv4NDyC/jeep.png",
        "https://i.postimg.cc/bryBJSrT/kia.png",
        "https://uploaddeimagens.com.br/images/004/873/725/thumb/lamborghini.png",
        "https://uploaddeimagens.com.br/images/004/873/724/thumb/lancia.png",
        "https://uploaddeimagens.com.br/images/004/873/723/thumb/land_rover.png",
        "https://uploaddeimagens.com.br/images/004/873/706/thumb/lexus.png",
        "https://uploaddeimagens.com.br/images/004/873/707/thumb/lincoln.png",
        "https://uploaddeimagens.com.br/images/004/873/708/thumb/maserati.png",
        "https://uploaddeimagens.com.br/images/004/873/722/thumb/mazda.png",
        "https://uploaddeimagens.com.br/images/004/873/705/thumb/mercedes.png",
        "https://uploaddeimagens.com.br/images/004/873/721/thumb/mercury.png",
        "https://uploaddeimagens.com.br/images/004/873/709/thumb/mini.png",
        "https://uploaddeimagens.com.br/images/004/873/710/thumb/mitsubishi.png",
        "https://uploaddeimagens.com.br/images/004/873/720/thumb/moskvitch.png",
        "https://uploaddeimagens.com.br/images/004/873/711/thumb/nissan.png",
        "https://uploaddeimagens.com.br/images/004/873/712/thumb/opel.png",
        "https://uploaddeimagens.com.br/images/004/873/719/thumb/peugeot.png",
        "https://uploaddeimagens.com.br/images/004/873/718/thumb/pontiac.png",
        "https://uploaddeimagens.com.br/images/004/873/717/thumb/porche.png",
        "https://uploaddeimagens.com.br/images/004/873/716/thumb/renault.png",
        "https://uploaddeimagens.com.br/images/004/873/713/thumb/rolls_royce.png",
        "https://uploaddeimagens.com.br/images/004/873/714/thumb/rover.png",
        "https://uploaddeimagens.com.br/images/004/873/715/thumb/saab.png",
        "https://uploaddeimagens.com.br/images/004/874/114/thumb/scion.png",
        "https://uploaddeimagens.com.br/images/004/874/126/thumb/seat.png",
        "https://uploaddeimagens.com.br/images/004/874/125/thumb/skoda.png",
        "https://uploaddeimagens.com.br/images/004/874/115/thumb/ssangyong.png",
        "https://uploaddeimagens.com.br/images/004/874/117/thumb/subaru.png",
        "https://uploaddeimagens.com.br/images/004/874/124/thumb/suzuki.png",
        "https://uploaddeimagens.com.br/images/004/874/123/thumb/tesla.png",
        "https://uploaddeimagens.com.br/images/004/874/121/thumb/toyota.png",
        "https://uploaddeimagens.com.br/images/004/874/122/thumb/uaz.png",
        "https://uploaddeimagens.com.br/images/004/874/116/thumb/vaz.png",
        "https://uploaddeimagens.com.br/images/004/874/120/thumb/volkswagem.png",
        "https://uploaddeimagens.com.br/images/004/874/119/thumb/volvo.png",
        "https://uploaddeimagens.com.br/images/004/874/118/thumb/zaz.png"
    ]
}

df = pd.DataFrame(data_marca)

st.write("### Filtros")

st.write(f"""<h5 style='color:yellow; font-size:15px;'> Ponto de melhoria 1: Realizar o pré processamento dos dados e aplicação apenas para o melhor modelo, neste caso o Radom Forest, atualmente o modelo esta lendo os três tipos e isso está demandando muito tempo de carregamento, ou seja, faz-se necessário separá-los, compará-los e depois aplicar apenas com um deles. </h5>""", unsafe_allow_html=True)
st.write(f"""<h5 style='color:yellow; font-size:15px;'> Ponto de melhoria 2: Aplicação de hiperparâmetros, visando melhorar o préprocessamento dos dados. </h5>""", unsafe_allow_html=True)
st.write(f"""<h5 style='color:yellow; font-size:15px;'> Ponto de melhoria 3: Experimentar o aumento do percentual de teste sobre a base para ver como se comporta as métricas . </h5>""", unsafe_allow_html=True)

# Filtros
fabricante = st.selectbox("Selecione o Fabricante:", sorted(df["fabricante"].unique()))
filtered_data = df[df["fabricante"] == fabricante]

# Exibe a logo do fabricante
st.write("Logo marca Fabricante:")
url_logo = filtered_data["logo"].values[0]
st.image(url_logo, width=100)

filtered_data = df_tratado[df_tratado["Fabricante"] == fabricante]

# Filtro modelo
modelo = st.selectbox("Selecione o Modelo:", sorted(filtered_data["Modelo"].unique()))
filtered_data = filtered_data[filtered_data["Modelo"] == modelo]

# Filtro categoria
categoria = st.selectbox("Selecione a Categoria:", sorted(filtered_data["Categoria"].unique()))
filtered_data = filtered_data[filtered_data["Categoria"] == categoria]

# Filtro tipo de combustível
tipo_combustivel = st.selectbox("Selecione o Tipo de Combustível:", sorted(filtered_data["Tipo de Combustível"].unique()))
filtered_data = filtered_data[filtered_data["Tipo de Combustível"] == tipo_combustivel]

# Filtro câmbio
tipo_cambio = st.selectbox("Selecione o Tipo de Câmbio:", sorted(filtered_data["Tipo de Câmbio"].unique()))
filtered_data = filtered_data[filtered_data["Tipo de Câmbio"] == tipo_cambio]

# Filtro ano
ano = st.selectbox("Selecione o Ano:", sorted(filtered_data["Ano"].unique()))
filtered_data = filtered_data[filtered_data["Ano"] == ano]

# Filtro tração
tracao = st.selectbox("Selecione a Tração:", sorted(filtered_data["Tração"].unique()))
filtered_data = filtered_data[filtered_data["Tração"] == tracao]

# Filtro Airbags
Airbags = st.selectbox("Selecione a quantidade de Airbags:", sorted(filtered_data["Airbags"].unique()))
filtered_data = filtered_data[filtered_data["Airbags"] == Airbags]

# Filtro Portas
Portas = st.selectbox("Selecione a quantidade de Portas:", sorted(filtered_data["Portas"].unique()))
filtered_data = filtered_data[filtered_data["Portas"] == Portas]

# Filtro Tamanho do Motor
t_motor = st.selectbox("Selecione Tamanho do Motor", sorted(filtered_data["Tamanho do Motor"].unique()))
filtered_data = filtered_data[filtered_data["Tamanho do Motor"] == t_motor]

# Filtro Cilindros
Cilindros = st.selectbox("Selecione a quantidade de Cilindros:", sorted(filtered_data["Cilindros"].unique()))
filtered_data = filtered_data[filtered_data["Cilindros"] == Cilindros]

# Slider do Imposto ajustado ao intervalo do DataFrame filtrado
Imposto_min = df_tratado["Imposto"].min()
Imposto_max = df_tratado["Imposto"].max()
Imposto = st.number_input("Defina o Imposto do veículo", min_value=Imposto_min, max_value=Imposto_max, value=Imposto_min)

# Slider de quilometragem ajustado ao intervalo do DataFrame filtrado
km_min = df_tratado["Quilometragem"].min()
km_max = df_tratado["Quilometragem"].max()
quilometragem = st.number_input("Defina a quilometragem do veículo", min_value=km_min, max_value=km_max, value=km_min)

# Filtrando os dados
filtered_data = df_tratado[
    (df_tratado["Fabricante"] == fabricante) &
    (df_tratado["Modelo"] == modelo) &
    (df_tratado["Categoria"] == categoria) &
    (df_tratado["Tipo de Combustível"] == tipo_combustivel) &
    (df_tratado["Tipo de Câmbio"] == tipo_cambio) &
    (df_tratado["Ano"] == ano) &
    (df_tratado["Tração"] == tracao) &
    (df_tratado["Portas"] == Portas) &
    (df_tratado["Airbags"] == Airbags) &
    (df_tratado["Tamanho do Motor"] == t_motor) &
    (df_tratado["Cilindros"] == Cilindros) &
    (df_tratado["Imposto"] <= Imposto) &
    (df_tratado["Quilometragem"] <= quilometragem) 

]

# Verificação para evitar erros se não houver dados filtrados
#if filtered_data.empty:
#   st.warning("Não há dados disponíveis para a seleção atual.")
#else:
#    st.write("### Dados Filtrados")
#    st.dataframe(filtered_data)

st.write("---")

# Preço Médio
preco_medio = df_tratado["Preço"].mean() if df_tratado["Preço"].mean() > 0 else 0.0
st.markdown(
    f"### <span style='color:yellow'>**Preço Médio - PM:**</span> "
    f"<span style='color:#4894CA'>${preco_medio:.2f}</span>",
    unsafe_allow_html=True
)

st.write("---")
#st.write(best_model)
#st.write(df_tratado.dtypes)

def predict_price(fabricante, modelo, categoria, ano, tipo_combustivel, tipo_cambio, tracao, quilometragem, Airbags, Cilindros, Imposto, Portas, t_motor):
    # Dicionário para mapear as opções de seleção para variáveis categóricas
    input_data = {
        'Imposto': Imposto,
        'Fabricante': fabricante,
        'Modelo': modelo,
        'Ano': ano,
        'Categoria': categoria,
        'Tipo de Combustível': tipo_combustivel,
        'Tamanho do Motor': t_motor,
        'Quilometragem': quilometragem,
        'Cilindros': Cilindros,
        'Tipo de Câmbio': tipo_cambio,
        'Tração': tracao,
        'Portas': Portas,
        'Airbags':Airbags
           
    }

    # Convertendo as seleções do usuário para uma estrutura de dados que o modelo entende
    input_df = pd.DataFrame([input_data])

    # Verificar se todas as colunas categóricas estão no input_df
    for col in categorical_columns:
        if col not in input_df.columns:
            st.error(f"Falta a coluna categórica {col} nos dados de entrada.")
            return None

    # Codificar as variáveis categóricas com o OneHotEncoder
    input_encoded = encoder.transform(input_df[categorical_columns])

    # Converter os dados de entrada para o formato correto
    input_final = pd.concat(
        [input_df.drop(columns=categorical_columns), 
         pd.DataFrame(input_encoded, columns=encoder.get_feature_names_out(categorical_columns))],
        axis=1
    )

    # Fazer a previsão usando o melhor modelo
    predicted_price = model_1.predict(input_final)

    return predicted_price[0]

# Previsão de preço
preco_estimado = predict_price(fabricante, modelo, categoria, ano, tipo_combustivel, tipo_cambio, tracao, quilometragem, Airbags, Cilindros, Imposto, Portas, t_motor)
if preco_estimado is not None:
    st.markdown(
        f"### <span style='color:yellow'>**Preço Sugerido - PS:**</span> "
         f"<span style='color:#4894CA'>$ {preco_estimado:.2f}</span>",
        unsafe_allow_html=True
    )
ps = preco_estimado
st.write("---")

# Preço Anúncio
preco_anuncio = st.number_input("Preço Anúncio - PA:", min_value=0.0, value=0.0, step=1000.0)
st.markdown(
    f"### <span style='color:yellow'>**Preço Anúncio - PA:**</span> "
    f"<span style='color:#4894CA'>$ {preco_anuncio:.2f}</span>",
    unsafe_allow_html=True
)

# Calcular margem do preço anúncio
if preco_medio > 0:  # Evitar divisão por zero
    margem_preco_anuncio = (preco_anuncio - preco_medio) / preco_medio * 100
    st.write("Margem Preço Anúncio: {margem_preco_anuncio:.2f}%")

####################################### 7. INTEGRAÇÃO MODELO DE CLASSIFICAÇÃO E MATRIZ DE CONFUSÃO ###########

erro = """"
y_true_class = ps 
y_pred_class = ps

# Gerando a matriz de confusão
conf_matrix = confusion_matrix(y_true_class, y_pred_class)

# Exibindo a matriz de confusão no Streamlit
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=["Preço ruim", "Preço bom"])

# Plotando a matriz de confusão
fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(ax=ax, cmap="Blues")
st.pyplot(fig)

# Cálculo das métricas de performance
accuracy = (conf_matrix[0, 0] + conf_matrix[1, 1]) / conf_matrix.sum()
precision = conf_matrix[1, 1] / (conf_matrix[1, 1] + conf_matrix[0, 1])
recall = conf_matrix[1, 1] / (conf_matrix[1, 1] + conf_matrix[1, 0])
f1 = 2 * (precision * recall) / (precision + recall)

st.write(f"### Métricas de Performance:")
st.write(f"**Acurácia:** {accuracy:.2f}")
st.write(f"**Precisão:** {precision:.2f}")
st.write(f"**Recall:** {recall:.2f}")
st.write(f"**F1 Score:** {f1:.2f}")

# Exibindo as previsões de preço bom ou ruim
st.write("### Previsões de Preço bom ou ruim")

# Exibindo os primeiros resultados como exemplo
resultados = pd.DataFrame({
    'Preço Real': y_true_class,
    'Preço Previsto': y_pred_class,
    'Classificação Real': y_true_class.map({0: 'Preço ruim', 1: 'Preço bom'}),
    'Classificação Prevista': y_pred_class.map({0: 'Preço ruim', 1: 'Preço bom'})
})
st.write(resultados.head(10))

# Recomendações com base na acurácia
if accuracy > 0.8:
    st.write("O modelo está funcionando bem! A recomendação de preço é confiável.")
else:
    st.write("O modelo pode precisar de ajustes. A recomendação de preço pode não ser precisa o suficiente.")

#"""