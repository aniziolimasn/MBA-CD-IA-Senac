Previsão de Preços de Veículos com Machine Learning
Este projeto tem como objetivo desenvolver uma solução completa para previsão de preços de veículos, utilizando técnicas de Machine Learning e visualização interativa com Streamlit. O sistema permite ao usuário simular cenários, analisar fatores que influenciam o valor dos veículos e obter recomendações de preço personalizadas.

Funcionalidades
Pipeline completo de Machine Learning: Extração, limpeza, pré-processamento, treinamento, avaliação e comparação de modelos de regressão.
Modelos utilizados: Random Forest, Regressão Linear e Árvore de Decisão.
Visualização interativa: Dashboard em Streamlit para análise dos dados, filtros dinâmicos e simulação de cenários.
Recomendações de preço: Previsão personalizada baseada nas características selecionadas pelo usuário.
Métricas de avaliação: MSE, R² e validação cruzada para comparação dos modelos.

Como utilizar

### Pré-requisitos:

- Python 3.8+
- Instalar as dependências listadas em `requirements.txt`:

```
pip install -r requirements.txt
```

Ou, se preferir instalar manualmente:

```
pip install pandas numpy scikit-learn streamlit matplotlib seaborn
```

### Execução:

Execute o script principal com o comando:

```
streamlit run car1.py
```

Acesse o dashboard pelo navegador, conforme instruções do Streamlit.

Personalização:

O usuário pode selecionar fabricante, modelo, categoria, tipo de combustível, câmbio, ano, tração, número de portas, airbags, tamanho do motor, cilindros, imposto e quilometragem para simular diferentes cenários de precificação.
Estrutura do Projeto
car1.py: Script principal com todo o pipeline de dados, modelagem e interface Streamlit.
car_price_prediction.csv: Base de dados utilizada (disponível no Kaggle).
Outras pastas e arquivos de apoio para logs, testes e documentação.
Pontos de melhoria
Automatizar a extração dos dados diretamente do Kaggle.
Otimizar o pipeline para treinar apenas o melhor modelo.
Aplicar ajuste de hiperparâmetros e análise de correlação para seleção de variáveis.
Melhorar a performance e modularização do código.
Créditos
Projeto desenvolvido para a disciplina de Machine Learning do MBA em Ciência de Dados e Inteligência Artificial - Faculdade SENAC/PE.

Se quiser, posso adaptar o texto para um formato mais resumido ou detalhado, conforme sua necessidade! - Acesse o dashboard pelo navegador, conforme instruções do Streamlit.

Personalização:
O usuário pode selecionar fabricante, modelo, categoria, tipo de combustível, câmbio, ano, tração, número de portas, airbags, tamanho do motor, cilindros, imposto e quilometragem para simular diferentes cenários de precificação.
Estrutura do Projeto
car1.py: Script principal com todo o pipeline de dados, modelagem e interface Streamlit.
car_price_prediction.csv: Base de dados utilizada (disponível no Kaggle).
Outras pastas e arquivos de apoio para logs, testes e documentação.