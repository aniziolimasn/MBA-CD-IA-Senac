# README - Geração de Postagens Publicitárias com IA

## Descrição

Este projeto é um aplicativo desenvolvido em Python utilizando Streamlit para geração automática de postagens publicitárias para redes sociais. Ele integra modelos de Inteligência Artificial hospedados na HuggingFace e OpenAI para:
- Gerar descrições automáticas de imagens (captioning)
- Criar imagens a partir de textos (text-to-image)
- Traduzir textos do inglês para o português
- Gerar sugestões de anúncios publicitários personalizados

## Funcionalidades
- **Upload de Imagem:** O usuário pode enviar uma imagem e receber uma descrição automática gerada por IA.
- **Geração de Imagem:** A partir de um texto, o app gera uma imagem correspondente.
- **Tradução:** Tradução automática de textos do inglês para o português brasileiro.
- **Sugestão de Anúncio:** Geração de textos publicitários curtos e otimizados para redes sociais, baseados em área de interesse e descrição.

## Tecnologias Utilizadas
- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [HuggingFace Hub](https://huggingface.co/)
- [OpenAI API](https://openai.com/)
- [Pillow (PIL)](https://python-pillow.org/)
- [Requests](https://docs.python-requests.org/)

## Como Executar
1. Clone este repositório:
   ```bash
   git clone <url-do-repositorio>
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```
4. Acesse o app pelo navegador no endereço exibido pelo Streamlit (geralmente http://localhost:8501).

## Estrutura do Projeto
- `app.py` - Código principal do aplicativo Streamlit
- `requirements.txt` - Lista de dependências do projeto

## Autores
- Anízio Neto
- Mario Souza
- Ivan Filho
- Gentil Ribeiro
- Vinicius Gomes

Faculdade SENAC/PE - MBA Ciência de Dados e IA - Deep Learning - Prof. Geraldo Gomes

## Observações
- É necessário possuir chaves de API válidas da HuggingFace e OpenAI para utilizar todas as funcionalidades.
- O projeto é para fins acadêmicos e demonstração de integração de IA generativa em aplicações práticas.
