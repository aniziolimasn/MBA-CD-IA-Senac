# README.md

# Projeto Big Date

Este projeto é uma aplicação em Python que busca dados de cotações de moedas em uma API, armazena esses dados em um banco de dados MongoDB e exibe as informações em uma interface web utilizando Streamlit. A aplicação é projetada para fornecer informações em tempo real sobre as cotações de moedas, permitindo que os usuários visualizem as últimas cotações e a evolução dos preços.

## Funcionalidades

- Busca cotações de moedas em tempo real através de uma API.
- Armazena os dados em um banco de dados MongoDB.
- Exibe as cotações em uma interface web interativa utilizando Streamlit.
- Atualizações automáticas das cotações a cada 30 segundos.

## Estrutura do Projeto

O projeto contém os seguintes arquivos:

- `app_big_date.py`: Unifica a lógica dos arquivos `front.py` e `back.py`, implementando a busca e exibição das cotações.
- `requirements.txt`: Lista as dependências necessárias para o projeto.
- `README.md`: Documentação do projeto.

## Instalação

Para instalar as dependências necessárias, execute o seguinte comando:

```
pip install -r requirements.txt
```

## Execução

Para executar a aplicação, utilize o seguinte comando:

```
streamlit run app_big_data.py
```

Certifique-se de que as variáveis de conexão com o MongoDB estão configuradas corretamente no código, garantindo a segurança das credenciais.

## Dependências

As principais dependências do projeto incluem:

- `streamlit`: Para a criação da interface web.
- `pymongo`: Para a interação com o banco de dados MongoDB.
- `pandas`: Para manipulação e análise de dados.
- `requests`: Para realizar requisições HTTP à API de cotações.
- `altair`: Para a criação de gráficos interativos.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.

## Licença

Este projeto é de código aberto e pode ser utilizado e modificado livremente.