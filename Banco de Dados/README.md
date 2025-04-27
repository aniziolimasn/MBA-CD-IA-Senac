# Scripts SQL – Projeto Loja de Roupas

Este diretório contém os scripts SQL utilizados para a criação, povoamento e automação do banco de dados do projeto **Loja de Roupas**. O objetivo é fornecer um ambiente de dados completo para simulação, testes e estudos acadêmicos.

## Estrutura dos Arquivos

### 1. `DDL - CRIACAO DB.sql`
Script de criação do banco de dados e de todas as tabelas, com comentários explicativos sobre cada entidade e relacionamento.

### 2. `DML - POVOANDO O BANCO.sql`
Script de inserção de dados iniciais (mock) em todas as tabelas, permitindo simulações e testes de consultas.

### 3. `DML - TRIGGER - PROCEDURE - COMPRAS.sql`
Script que automatiza a movimentação de estoque ao registrar compras, utilizando procedures e triggers.

### 4. `DML - TRIGGER - PROCEDURE - VENDAS.sql`
Script que automatiza a movimentação de estoque ao registrar vendas, utilizando procedures e triggers.

## Finalidade

- Automatizar o controle de estoque, garantindo integridade e rastreabilidade das movimentações.
- Facilitar o aprendizado de conceitos de banco de dados relacional, procedures, triggers e manipulação de dados.
- Servir como base para projetos acadêmicos, estudos ou demonstrações.

## Observações

- Os scripts estão documentados e prontos para uso em ambientes MySQL.
- **Ordem recomendada para execução dos scripts**:
  1. `DDL - CRIACAO DB.sql`
  2. `DML - POVOANDO O BANCO.sql`
  3. `DML - TRIGGER - PROCEDURE - COMPRAS.sql`
  4. `DML - TRIGGER - PROCEDURE - VENDAS.sql`
- Caso utilize outro nome de banco de dados, ajuste os scripts conforme necessário.
- Todos os dados inseridos são fictícios e utilizados apenas para fins de teste.

