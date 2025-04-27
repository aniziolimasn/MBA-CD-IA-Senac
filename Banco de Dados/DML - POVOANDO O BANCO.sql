-- ------------------------------------------------------------
-- Script de Povoamento do Banco de Dados db_lojaroupa
-- Finalidade: Inserir dados iniciais (mock) para simulação e testes
-- Autor: Anizio Neto
-- Data: 18/07/2024
-- ------------------------------------------------------------

-- Tabela: categorias
-- Descrição: Armazena os tipos de categorias de produtos vendidos na loja.
-- Exemplo: Camisas, Calças, Sapatos, etc.
-- Utilidade: Facilita a classificação e filtragem dos produtos.
-- ------------------------------------------------------------
-- Inserção de dados na tabela `categorias`
INSERT INTO `db_lojaroupa`.`categorias` (`desc_categoria`) VALUES
('Camisas'),
('Calças'),
('Sapatos'),
('Acessórios'),
('Vestidos');

-- Tabela: remuneracao
-- Descrição: Define os tipos de remuneração dos funcionários e o percentual de comissão.
-- Utilidade: Permite diferenciar salários fixos, comissionados e mistos.
-- ------------------------------------------------------------
-- Inserção de dados na tabela `remuneracao`
INSERT INTO `db_lojaroupa`.`remuneracao` (`tipo_remuneracao`, `percentual_comissao`) VALUES
('Salário Fixo', 0.00),
('Comissionado', 0.10),
('Misto', 0.05);

-- Tabela: funcionarios
-- Descrição: Cadastro dos funcionários da loja, com dados pessoais, cargo, formação, cidade, UF, endereço e tipo de remuneração.
-- Utilidade: Gerenciar equipe, folha de pagamento e alocação de funções.
-- ------------------------------------------------------------
-- Inserção de dados na tabela `funcionarios`
INSERT INTO `db_lojaroupa`.`funcionarios` (`nome`, `cpf`, `data_nasc`, `sexo`, `data_admissao`, `cargo`, `formacao`, `url_imagem`, `cidade`, `uf`, `endereco`, `remuneracao_id_remuneracao`) VALUES
('Anizio Neto', '11111111111', '1980-01-01', 'M', '2020-01-01', 'Analista', 'Informática', NULL, 'São Paulo', 'SP', 'Rua A, 123', 1),
('Gentil Ribeiro', '22222222222', '1985-02-02', 'M', '2021-02-02', 'Analista', 'Informática', NULL, 'Rio de Janeiro', 'RJ', 'Rua B, 456', 2),
('Vinicius Gomes', '33333333333', '1990-03-03', 'M', '2022-03-03', 'Vendedor', 'Informática', NULL, 'Belo Horizonte', 'MG', 'Rua C, 789', 3),
('Mario Souza', '44444444444', '1995-04-04', 'M', '2023-04-04', 'Vendedor', 'Informática', NULL, 'Curitiba', 'PR', 'Rua D, 101', 1),
('Jedson Moura', '55555555555', '2000-05-05', 'M', '2024-05-05', 'Vendedor', 'Informática', NULL, 'Porto Alegre', 'RS', 'Rua E, 202', 2),
('Ivan Filho', '66666666666', '2005-06-06', 'M', '2025-06-06', 'Vendedor', 'Informática', NULL, 'Salvador', 'BA', 'Rua F, 303', 3),
('Carlos Silva', '77777777777', '1988-07-07', 'M', '2026-07-07', 'Gerente de Vendas', 'Administração', NULL, 'Brasília', 'DF', 'Rua G, 404', 1),
('Ana Pereira', '88888888888', '1982-08-08', 'F', '2027-08-08', 'Assistente de Marketing', 'Marketing', NULL, 'Fortaleza', 'CE', 'Rua H, 505', 2),
('Beatriz Lima', '99999999999', '1991-09-09', 'F', '2028-09-09', 'Coordenadora de RH', 'Recursos Humanos', NULL, 'Manaus', 'AM', 'Rua I, 606', 3),
('Fernando Costa', '12121212121', '1983-10-10', 'M', '2029-10-10', 'Supervisor de Loja', 'Engenharia', NULL, 'Belém', 'PA', 'Rua J, 707', 1),
('Gabriela Rocha', '13131313131', '1986-11-11', 'F', '2030-11-11', 'Analista Financeira', 'Economia', NULL, 'Goiânia', 'GO', 'Rua K, 808', 2),
('Heitor Mendes', '14141414141', '1993-12-12', 'M', '2031-12-12', 'Desenvolvedor de Sistemas', 'Informática', NULL, 'Recife', 'PE', 'Rua L, 909', 3),
('Juliana Faria', '15151515151', '1987-01-13', 'F', '2032-01-13', 'Designer de Moda', 'Design Gráfico', NULL, 'Natal', 'RN', 'Rua M, 1010', 1),
('Lucas Fernandes', '16161616161', '1992-02-14', 'M', '2033-02-14', 'Engenheiro de Produção', 'Engenharia Civil', NULL, 'São Luís', 'MA', 'Rua N, 1111', 2),
('Mariana Oliveira', '17171717171', '1984-03-15', 'F', '2034-03-15', 'Consultora de Vendas', 'Consultoria', NULL, 'João Pessoa', 'PB', 'Rua O, 1212', 3),
('Nicolas Santos', '18181818181', '1995-04-16', 'M', '2035-04-16', 'Técnico de Manutenção', 'Mecânica', NULL, 'Aracaju', 'SE', 'Rua P, 1313', 1);

-- Tabela: cliente
-- Descrição: Cadastro de clientes, podendo ser pessoa física (PF) ou jurídica (PJ), com dados de contato, endereço, status, etc.
-- Utilidade: Gerenciar vendas, promoções, relacionamento e histórico de compras.
-- ------------------------------------------------------------
-- Inserção de dados na tabela `cliente`
INSERT INTO `db_lojaroupa`.`cliente` (`nome_cliente`, `tipo_cliente`, `cpf_cnpj`, `uf`, `cidade`, `endereco`, `teleforne`, `e-mail`, `data_cadastro`, `status_cliente`) VALUES
('Cliente A', 'PF', '11111111111', 'SP', 'São Paulo', 'Rua X, 123', '11999999999', 'clienteA@example.com', '2023-01-01', 'Ativo'),
('Cliente B', 'PJ', '22222222222222', 'RJ', 'Rio de Janeiro', 'Rua Y, 456', '21999999999', 'clienteB@example.com', '2023-02-01', 'Inativo'),
('Cliente C', 'PF', '33333333333', 'MG', 'Belo Horizonte', 'Rua Z, 789', '31999999999', 'clienteC@example.com', '2023-03-01', 'Ativo'),
('Cliente D', 'PF', '44444444444', 'RS', 'Porto Alegre', 'Rua W, 101', '51999999999', 'clienteD@example.com', '2023-04-01', 'Ativo'),
('Cliente E', 'PJ', '55555555555555', 'BA', 'Salvador', 'Rua V, 202', '71999999999', 'clienteE@example.com', '2023-05-01', 'Inativo'),
('Cliente F', 'PF', '66666666666', 'PR', 'Curitiba', 'Rua U, 303', '41999999999', 'clienteF@example.com', '2023-06-01', 'Ativo'),
('Cliente G', 'PF', '77777777777', 'SC', 'Florianópolis', 'Rua T, 404', '48999999999', 'clienteG@example.com', '2023-07-01', 'Inativo'),
('Cliente H', 'PF', '88888888888', 'AM', 'Manaus', 'Rua S, 505', '92999999999', 'clienteH@example.com', '2023-08-01', 'Ativo'),
('Cliente I', 'PJ', '99999999999999', 'PE', 'Recife', 'Rua R, 606', '81999999999', 'clienteI@example.com', '2023-09-01', 'Inativo'),
('Cliente J', 'PF', '10101010101', 'CE', 'Fortaleza', 'Rua Q, 707', '85999999999', 'clienteJ@example.com', '2023-10-01', 'Ativo'),
('Cliente K', 'PJ', '12121212121212', 'ES', 'Vitória', 'Rua P, 808', '27999999999', 'clienteK@example.com', '2023-11-01', 'Ativo'),
('Cliente L', 'PF', '13131313131', 'DF', 'Brasília', 'Rua O, 909', '61999999999', 'clienteL@example.com', '2023-12-01', 'Inativo'),
('Cliente M', 'PF', '14141414141', 'MT', 'Cuiabá', 'Rua N, 1010', '65999999999', 'clienteM@example.com', '2024-01-01', 'Ativo'),
('Cliente N', 'PJ', '15151515151515', 'GO', 'Goiânia', 'Rua M, 1111', '62999999999', 'clienteN@example.com', '2024-02-01', 'Ativo'),
('Cliente O', 'PF', '16161616161', 'MS', 'Campo Grande', 'Rua L, 1212', '67999999999', 'clienteO@example.com', '2024-03-01', 'Inativo'),
('Cliente P', 'PF', '17171717171', 'AL', 'Maceió', 'Rua K, 1313', '82999999999', 'clienteP@example.com', '2024-04-01', 'Ativo'),
('Cliente Q', 'PJ', '18181818181818', 'PB', 'João Pessoa', 'Rua J, 1414', '83999999999', 'clienteQ@example.com', '2024-05-01', 'Ativo'),
('Cliente R', 'PF', '19191919191', 'RN', 'Natal', 'Rua I, 1515', '84999999999', 'clienteR@example.com', '2024-06-01', 'Inativo'),
('Cliente S', 'PF', '20202020202', 'RO', 'Porto Velho', 'Rua H, 1616', '69999999999', 'clienteS@example.com', '2024-07-01', 'Ativo'),
('Cliente T', 'PJ', '21212121212121', 'TO', 'Palmas', 'Rua G, 1717', '63999999999', 'clienteT@example.com', '2024-08-01', 'Ativo');

-- Inserção de dados na tabela `impostos`
INSERT INTO `db_lojaroupa`.`impostos` (`nome_imposto`, `perc_aliquota`) VALUES
('ICMS', 18.00),
('IPI', 5.00),
('PIS', 1.65),
('COFINS', 7.60);

-- Inserção de dados na tabela `fornecedor`
INSERT INTO `db_lojaroupa`.`fornecedor` (`nome_fornecedor`, `tipo_fornecedor`, `cpf_cnpj`, `uf`, `cidade`, `endereco`, `teleforne`, `e-mail`, `data_cadastro`, `status_fornecedor`) VALUES
('Fornecedor A', 'PJ', '33333333333333', 'MG', 'Belo Horizonte', 'Rua Z, 789', '31999999999', 'fornecedorA@example.com', '2023-01-01', 'Ativo'),
('Fornecedor B', 'PF', '44444444444', 'RS', 'Porto Alegre', 'Rua W, 101', '51999999999', 'fornecedorB@example.com', '2023-02-01', 'Ativo'),
('Fornecedor C', 'PJ', '55555555555555', 'SP', 'São Paulo', 'Rua X, 202', '11999999999', 'fornecedorC@example.com', '2023-03-01', 'Ativo'),
('Fornecedor D', 'PF', '66666666666', 'RJ', 'Rio de Janeiro', 'Rua Y, 303', '21999999999', 'fornecedorD@example.com', '2023-04-01', 'Ativo'),
('Fornecedor E', 'PJ', '77777777777777', 'PR', 'Curitiba', 'Rua V, 404', '41999999999', 'fornecedorE@example.com', '2023-05-01', 'Ativo'),
('Fornecedor F', 'PF', '88888888888', 'BA', 'Salvador', 'Rua U, 505', '71999999999', 'fornecedorF@example.com', '2023-06-01', 'Ativo'),
('Fornecedor G', 'PJ', '99999999999999', 'SC', 'Florianópolis', 'Rua T, 606', '48999999999', 'fornecedorG@example.com', '2023-07-01', 'Ativo'),
('Fornecedor H', 'PF', '10101010101', 'PE', 'Recife', 'Rua S, 707', '81999999999', 'fornecedorH@example.com', '2023-08-01', 'Ativo'),
('Fornecedor I', 'PJ', '11111111111111', 'CE', 'Fortaleza', 'Rua R, 808', '85999999999', 'fornecedorI@example.com', '2023-09-01', 'Ativo'),
('Fornecedor J', 'PF', '12121212121', 'GO', 'Goiânia', 'Rua Q, 909', '62999999999', 'fornecedorJ@example.com', '2023-10-01', 'Ativo'),
('Fornecedor K', 'PJ', '13131313131313', 'AM', 'Manaus', 'Rua P, 1010', '92999999999', 'fornecedorK@example.com', '2023-11-01', 'Ativo'),
('Fornecedor L', 'PF', '14141414141', 'PA', 'Belém', 'Rua O, 1111', '91999999999', 'fornecedorL@example.com', '2023-12-01', 'Ativo');

-- Inserção de dados na tabela `promo_desc`
INSERT INTO `db_lojaroupa`.`promo_desc` (`nome_promocao`, `perc_desconto`, `data_inicio`, `data_fim`) VALUES
('Promoção de Verão', 10.00, '2023-06-01', '2023-08-31'),
('Promoção de Inverno', 15.00, '2023-12-01', '2024-02-28');

-- Inserção de dados na tabela `canal`
INSERT INTO `db_lojaroupa`.`canal` (`nome_canal`) VALUES
('Loja Física'),
('E-commerce'),
('Telemarketing');

-- Inserção de dados na tabela `meios_pgto`
INSERT INTO `db_lojaroupa`.`meios_pgto` (`nome_meio_pgto`, `perc_taxa_adm`) VALUES
('Cartão de Crédito', 2.50),
('Boleto', 1.00),
('PIX', 0.50);

-- Inserção de dados na tabela `produtos`
INSERT INTO `db_lojaroupa`.`produtos` (`desc_produto`, `status_produto`, `data_cadastro`, `preco_custo`, `preco_venda`, `categorias_id_categoria`) VALUES
('Camiseta Branca', 'Disponível', '2023-01-01', 20.00, 30.00, 1),
('Calça Jeans', 'Disponível', '2023-02-01', 50.00, 80.00, 2),
('Tênis Esportivo', 'Indisponível', '2023-03-01', 100.00, 150.00, 3),
('Cinto de Couro', 'Disponível', '2023-04-01', 15.00, 25.00, 4),
('Vestido de Verão', 'Disponível', '2023-05-01', 60.00, 90.00, 5),
('Blusa de Frio', 'Disponível', '2023-06-01', 40.00, 70.00, 1),
('Saia Jeans', 'Disponível', '2023-07-01', 30.00, 50.00, 2),
('Sandália Feminina', 'Indisponível', '2023-08-01', 80.00, 120.00, 3),
('Boné Unissex', 'Disponível', '2023-09-01', 10.00, 20.00, 4),
('Camisa Social', 'Disponível', '2023-10-01', 45.00, 75.00, 5),
('Jaqueta de Couro', 'Disponível', '2023-11-01', 150.00, 200.00, 1),
('Calça de Moletom', 'Disponível', '2023-12-01', 35.00, 55.00, 2),
('Bota de Inverno', 'Indisponível', '2024-01-01', 120.00, 180.00, 3),
('Chapéu de Praia', 'Disponível', '2024-02-01', 25.00, 40.00, 4),
('Macacão Feminino', 'Disponível', '2024-03-01', 55.00, 85.00, 5);

-- Inserção de dados na tabela `mov_estoque`
INSERT INTO `db_lojaroupa`.`mov_estoque` (`data_movimentacao`, `produtos_id_produto`, `qtd_compra`, `qtd_venda`, `saldo_dia`, `saldo_anterior`, `estoque`) VALUES 
('2022-12-31', 1, 0, 0, 0, 0, 0),
('2022-12-31', 2, 0, 0, 0, 0, 0),
('2022-12-31', 3, 0, 0, 0, 0, 0),
('2022-12-31', 4, 0, 0, 0, 0, 0),
('2022-12-31', 5, 0, 0, 0, 0, 0),
('2022-12-31', 6, 0, 0, 0, 0, 0),
('2022-12-31', 7, 0, 0, 0, 0, 0),
('2022-12-31', 8, 0, 0, 0, 0, 0),
('2022-12-31', 9, 0, 0, 0, 0, 0),
('2022-12-31', 10, 0, 0, 0, 0, 0),
('2022-12-31', 11, 0, 0, 0, 0, 0),
('2022-12-31', 12, 0, 0, 0, 0, 0),
('2022-12-31', 13, 0, 0, 0, 0, 0),
('2022-12-31', 14, 0, 0, 0, 0, 0),
('2022-12-31', 15, 0, 0, 0, 0, 0);

-- Inserção de dados nas tabelas de `compras` e `vendas`

-- 2023-01-01 
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF001', 1, '2023-01-01', '2023-01-01', 1, 20, 20.00, 1, 1),
('NF001', 1, '2023-01-01', '2023-01-01', 1, 30, 50.00, 2, 1),
('NF001', 1, '2023-01-01', '2023-01-01', 1, 10, 100.00, 3, 1),
('NF001', 1, '2023-01-01', '2023-01-01', 1, 15, 15.00, 4, 1),
('NF001', 1, '2023-01-01', '2023-01-01', 1, 25, 60.00, 5, 1);
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(1, '2023-01-01', 'NF001', 1, 1, 1, 1, 2, 180.00, 1, 2, 10.80),
(1, '2023-01-01', 'NF001', 1, 1, 1, 1, 3, 270.00, 2, 2, 16.20);

-------------------------------------------------------
-- 2023-01-02
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(2, '2023-01-02', 'NF002', 2, 2, 2, 2, 1, 90.00, 3, 2, 5.40);

-------------------------------------------------------
-- 2023-02-01
-- COMPRA 
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF002', 1, '2023-02-01', '2023-02-01', 2, 50, 50.00, 2, 1),
('NF002', 1, '2023-02-01', '2023-02-01', 2, 20, 20.00, 1, 1),
('NF002', 1, '2023-02-01', '2023-02-01', 2, 30, 100.00, 3, 1),
('NF002', 1, '2023-02-01', '2023-02-01', 2, 15, 15.00, 4, 1),
('NF002', 1, '2023-02-01', '2023-02-01', 2, 40, 60.00, 5, 1);
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(3, '2023-02-01', 'NF003', 1, 3, 3, 3, 4, 360.00, 4, 2, 21.60),
(3, '2023-02-01', 'NF003', 1, 3, 3, 3, 2, 180.00, 5, 2, 10.80);

--------------------------------------------------------
-- 2023-02-02
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(4, '2023-02-02', 'NF004', 2, 1, 1, 4, 1, 60.00, 1, 2, 3.60),
(4, '2023-02-02', 'NF004', 2, 1, 1, 4, 3, 180.00, 2, 2, 10.80);

--------------------------------------------------------
-- 2023-03-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF003', 1, '2023-03-01', '2023-03-01', 3, 30, 100.00, 3, 1),
('NF003', 1, '2023-03-01', '2023-03-01', 3, 20, 20.00, 1, 1),
('NF003', 1, '2023-03-01', '2023-03-01', 3, 50, 50.00, 2, 1),
('NF003', 1, '2023-03-01', '2023-03-01', 3, 25, 15.00, 4, 1),
('NF003', 1, '2023-03-01', '2023-03-01', 3, 35, 60.00, 5, 1);
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(5, '2023-03-01', 'NF005', 1, 2, 2, 5, 2, 120.00, 3, 2, 7.20),
(5, '2023-03-01', 'NF005', 1, 2, 2, 5, 4, 240.00, 4, 2, 14.40);

--------------------------------------------------------
-- 2023-03-02
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(6, '2023-03-02', 'NF006', 2, 3, 3, 1, 1, 45.00, 5, 2, 2.70);

---------------------------------------------------------
-- 2023-04-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF004', 1, '2023-04-01', '2023-04-01', 4, 15, 15.00, 4, 1),
('NF004', 1, '2023-04-01', '2023-04-01', 4, 20, 20.00, 1, 1),
('NF004', 1, '2023-04-01', '2023-04-01', 4, 50, 50.00, 2, 1),
('NF004', 1, '2023-04-01', '2023-04-01', 4, 30, 100.00, 3, 1),
('NF004', 1, '2023-04-01', '2023-04-01', 4, 25, 60.00, 5, 1);
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(7, '2023-04-01', 'NF007', 1, 1, 1, 2, 3, 270.00, 1, 2, 16.20),
(7, '2023-04-01', 'NF007', 1, 1, 1, 2, 1, 90.00, 2, 2, 5.40);

---------------------------------------------------------
-- 2023-04-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(8, '2023-04-02', 'NF008', 2, 2, 2, 3, 2, 120.00, 3, 2, 7.20),
(8, '2023-04-02', 'NF008', 2, 2, 2, 3, 4, 240.00, 4, 2, 14.40);

----------------------------------------------------------
-- 2023-05-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF005', 1, '2023-05-01', '2023-05-01', 5, 40, 60.00, 5, 1),
('NF005', 1, '2023-05-01', '2023-05-01', 5, 50, 50.00, 2, 1),
('NF005', 1, '2023-05-01', '2023-05-01', 5, 30, 100.00, 3, 1),
('NF005', 1, '2023-05-01', '2023-05-01', 5, 20, 20.00, 1, 1),
('NF005', 1, '2023-05-01', '2023-05-01', 5, 15, 15.00, 4, 1);

-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(9, '2023-05-01', 'NF009', 1, 3, 3, 4, 1, 60.00, 5, 2, 3.60);

---------------------------------------------------------
-- 2023-05-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(10, '2023-05-02', 'NF010', 1, 1, 1, 5, 4, 360.00, 1, 2, 21.60),
(10, '2023-05-02', 'NF010', 1, 1, 1, 5, 2, 180.00, 2, 2, 10.80);

----------------------------------------------------------
-- 2023-06-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF006', 2, '2023-06-01', '2023-06-01', 1, 80, 20.00, 1, 2),
('NF006', 2, '2023-06-01', '2023-06-01', 1, 40, 60.00, 5, 2),
('NF006', 2, '2023-06-01', '2023-06-01', 1, 30, 100.00, 3, 2),
('NF006', 2, '2023-06-01', '2023-06-01', 1, 50, 50.00, 2, 2),
('NF006', 2, '2023-06-01', '2023-06-01', 1, 25, 15.00, 4, 2);

-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(11, '2023-06-01', 'NF011', 2, 2, 2, 1, 1, 45.00, 3, 2, 2.70);

---------------------------------------------------------
-- 2023-06-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(12, '2023-06-02', 'NF012', 1, 3, 3, 2, 3, 270.00, 4, 2, 16.20),
(12, '2023-06-02', 'NF012', 1, 3, 3, 2, 1, 90.00, 5, 2, 5.40);

---------------------------------------------------------
-- 2023-07-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF007', 2, '2023-07-01', '2023-07-01', 2, 60, 50.00, 2, 2),
('NF007', 2, '2023-07-01', '2023-07-01', 2, 40, 60.00, 5, 2),
('NF007', 2, '2023-07-01', '2023-07-01', 2, 80, 20.00, 1, 2),
('NF007', 2, '2023-07-01', '2023-07-01', 2, 30, 100.00, 3, 2),
('NF007', 2, '2023-07-01', '2023-07-01', 2, 25, 15.00, 4, 2);

-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(13, '2023-07-01', 'NF013', 2, 1, 1, 3, 2, 120.00, 1, 2, 7.20),
(13, '2023-07-01', 'NF013', 2, 1, 1, 3, 4, 240.00, 2, 2, 14.40);

----------------------------------------------------------
-- 2023-07-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(14, '2023-07-02', 'NF014', 1, 2, 2, 4, 1, 60.00, 3, 2, 3.60),
(14, '2023-07-02', 'NF014', 1, 2, 2, 4, 3, 180.00, 4, 2, 10.80);

-----------------------------------------------------------
-- 2023-08-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF008', 2, '2023-08-01', '2023-08-01', 3, 90, 100.00, 3, 2),
('NF008', 2, '2023-08-01', '2023-08-01', 3, 50, 50.00, 2, 2),
('NF008', 2, '2023-08-01', '2023-08-01', 3, 25, 15.00, 4, 2),
('NF008', 2, '2023-08-01', '2023-08-01', 3, 40, 60.00, 5, 2),
('NF008', 2, '2023-08-01', '2023-08-01', 3, 20, 20.00, 1, 2);

-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(15, '2023-08-01', 'NF015', 1, 3, 3, 5, 4, 360.00, 5, 2, 21.60),
(15, '2023-08-01', 'NF015', 1, 3, 3, 5, 2, 180.00, 1, 2, 10.80);

------------------------------------------------------------
-- 2023-09-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF009', 2, '2023-09-01', '2023-09-01', 4, 110, 15.00, 4, 2),
('NF009', 2, '2023-09-01', '2023-09-01', 4, 30, 100.00, 3, 2),
('NF009', 2, '2023-09-01', '2023-09-01', 4, 50, 50.00, 2, 2),
('NF009', 2, '2023-09-01', '2023-09-01', 4, 20, 20.00, 1, 2),
('NF009', 2, '2023-09-01', '2023-09-01', 4, 40, 60.00, 5, 2);

------------------------------------------------------------
-- 2023-10-01
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF010', 2, '2023-10-01', '2023-10-01', 5, 120, 60.00, 5, 2),
('NF010', 2, '2023-10-01', '2023-10-01', 5, 20, 20.00, 1, 2),
('NF010', 2, '2023-10-01', '2023-10-01', 5, 50, 50.00, 2, 2),
('NF010', 2, '2023-10-01', '2023-10-01', 5, 30, 100.00, 3, 2),
('NF010', 2, '2023-10-01', '2023-10-01', 5, 25, 15.00, 4, 2);

------------------------------------------------------------
-- 2023-11-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(16, '2023-11-02', 'NF016', 1, 1, 1, 2, 3, 180.00, 3, 2, 10.80),
(16, '2023-11-02', 'NF016', 1, 1, 1, 2, 1, 60.00, 4, 2, 3.60);

------------------------------------------------------------
-- 2023-12-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(18, '2023-12-02', 'NF018', 1, 3, 3, 4, 1, 80.00, 2, 2, 4.40),
(18, '2023-12-02', 'NF018', 1, 3, 3, 4, 3, 180.00, 3, 2, 12.60);

------------------------------------------------------------
-- 2024-01-01
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(19, '2024-01-01', 'NF019', 2, 1, 1, 5, 2, 135.00, 4, 2, 9.45),
(19, '2024-01-01', 'NF019', 2, 1, 1, 5, 1, 60.00, 5, 2, 4.50);

------------------------------------------------------------
-- 2024-01-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(20, '2024-01-02', 'NF020', 1, 2, 2, 1, 1, 45.00, 1, 2, 2.35),
(20, '2024-01-02', 'NF020', 1, 2, 2, 1, 2, 90.00, 2, 2, 5.85),
(20, '2024-01-02', 'NF020', 1, 2, 2, 1, 3, 120.00, 3, 2, 8.40);

-------------------------------------------------------------
-- 2024-02-01
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(9, '2024-02-01', 'NF021', 2, 3, 3, 2, 2, 120.00, 1, 2, 8.40),
(9, '2024-02-01', 'NF021', 2, 3, 3, 2, 4, 210.00, 5, 2, 15.75);

-------------------------------------------------------------
-- 2024-02-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(9, '2024-02-02', 'NF022', 1, 1, 1, 3, 3, 180.00, 3, 2, 10.80),
(9, '2024-02-02', 'NF022', 1, 1, 1, 3, 1, 60.00, 4, 2, 3.60);

-------------------------------------------------------------
-- 2024-03-01
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(9, '2024-03-01', 'NF023', 2, 2, 2, 4, 4, 210.00, 5, 2, 15.75),
(9, '2024-03-01', 'NF023', 2, 2, 2, 4, 2, 120.00, 1, 2, 8.40);

-------------------------------------------------------------
-- 2024-03-02
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(9, '2024-03-02', 'NF024', 1, 3, 3, 5, 1, 80.00, 2, 2, 4.40),
(9, '2024-03-02', 'NF024', 1, 3, 3, 5, 3, 180.00, 3, 2, 12.60);

-------------------------------------------------------------
-- 2024-04-01
-- VENDA 
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(9, '2024-04-01', 'NF025', 2, 1, 1, 1, 2, 135.00, 4, 2, 9.45),
(9, '2024-04-01', 'NF025', 2, 1, 1, 1, 1, 60.00, 5, 2, 4.50);

-- 2024-04-02
-- COMPRA
INSERT INTO db_lojaroupa.compra (nf_fornecedor, fornecedor_id_fornecedor, data_compra, data_emissao_nf, funcionarios_id_funcionarios, qtd_compra, preco_compra, produtos_id_produto, impostos_id_impostos)
VALUES
('NF008', 1, '2024-04-02', '2024-04-02', 1, 50, 45.00, 1, 1),
('NF009', 2, '2024-04-02', '2024-04-02', 2, 30, 55.00, 2, 2),
('NF010', 1, '2024-04-02', '2024-04-02', 3, 40, 60.00, 3, 3),
('NF011', 2, '2024-04-02', '2024-04-02', 4, 70, 25.00, 4, 1),
('NF012', 1, '2024-04-02', '2024-04-02', 5, 90, 30.00, 5, 2),
('NF013', 2, '2024-04-02', '2024-04-02', 1, 20, 40.00, 1, 3),
('NF014', 1, '2024-04-02', '2024-04-02', 2, 60, 45.00, 2, 1),
('NF015', 2, '2024-04-02', '2024-04-02', 3, 50, 55.00, 3, 2),
('NF016', 1, '2024-04-02', '2024-04-02', 4, 30, 35.00, 4, 3),
('NF017', 2, '2024-04-02', '2024-04-02', 5, 40, 25.00, 5, 1);

-- 2024-04-03
-- VENDA
INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(1, '2024-04-03', 'NF026', 1, 1, 1, 1, 5, 150.00, 1, 1, 10.00),
(2, '2024-04-03', 'NF027', 1, 1, 1, 2, 10, 300.00, 2, 2, 20.00),
(3, '2024-04-04', 'NF028', 2, 2, 2, 3, 15, 450.00, 3, 3, 30.00),
(4, '2024-04-04', 'NF029', 2, 2, 2, 1, 20, 600.00, 4, 1, 40.00),
(5, '2024-04-05', 'NF030', 1, 1, 1, 2, 25, 750.00, 5, 2, 50.00),
(6, '2024-04-05', 'NF031', 1, 1, 1, 1, 30, 900.00, 1, 3, 60.00),
(7, '2024-04-06', 'NF032', 2, 2, 2, 2, 35, 1050.00, 2, 1, 70.00),
(8, '2024-04-06', 'NF033', 2, 2, 2, 3, 40, 1200.00, 3, 2, 80.00),
(9, '2024-04-07', 'NF034', 1, 1, 1, 4, 45, 1350.00, 4, 3, 90.00),
(10, '2024-04-07', 'NF035', 1, 1, 1, 1, 50, 1500.00, 5, 1, 100.00),
(11, '2024-04-08', 'NF036', 2, 2, 2, 1, 55, 1650.00, 1, 2, 110.00),
(12, '2024-04-08', 'NF037', 2, 2, 2, 2, 60, 1800.00, 2, 3, 120.00),
(13, '2024-04-09', 'NF038', 1, 1, 1, 3, 65, 1950.00, 3, 1, 130.00),
(14, '2024-04-09', 'NF039', 1, 1, 1, 2, 70, 2100.00, 4, 2, 140.00),
(15, '2024-04-10', 'NF040', 2, 2, 2, 3, 75, 2250.00, 5, 3, 150.00),
(16, '2024-04-10', 'NF041', 2, 2, 2, 1, 80, 2400.00, 1, 1, 160.00),
(17, '2024-04-11', 'NF042', 1, 1, 1, 2, 85, 2550.00, 2, 2, 170.00),
(18, '2024-04-11', 'NF043', 1, 1, 1, 3, 90, 2700.00, 3, 3, 180.00),
(19, '2024-04-12', 'NF044', 2, 2, 2, 1, 95, 2850.00, 4, 1, 190.00),
(1, '2024-04-12', 'NF045', 2, 2, 2, 2, 100, 3000.00, 5, 2, 200.00);

INSERT INTO db_lojaroupa.venda (cliente_id_cliente, data_emissao_nf, nf_venda, promo_desc_id_promo_desc, meios_pgto_id_meio_pgto, canal_id_canal, funcionarios_id_funcionarios, qtd_venda, preco_venda, produtos_id_produto, impostos_id_impostos, valor_imposto)
VALUES
(1, '2024-04-12', 'NF084', 1, 1, 1, 1, 7, 210.00, 1, 1, 14.70),
(2, '2024-04-12', 'NF085', 1, 1, 1, 1, 8, 240.00, 2, 1, 16.80),
(3, '2024-04-12', 'NF086', 2, 2, 2, 2, 6, 180.00, 3, 2, 12.60),
(4, '2024-04-12', 'NF087', 2, 2, 2, 1, 9, 270.00, 4, 2, 18.90),
(5, '2024-04-12', 'NF088', 2, 1, 1, 3, 10, 300.00, 5, 3, 21.00),
(6, '2024-04-12', 'NF089', 2, 2, 2, 2, 5, 150.00, 1, 3, 10.50),
(7, '2024-04-12', 'NF090', 1, 1, 1, 1, 4, 120.00, 2, 1, 8.40),
(8, '2024-04-12', 'NF091', 2, 1, 1, 2, 7, 210.00, 3, 2, 14.70),
(9, '2024-04-12', 'NF092', 2, 2, 2, 2, 3, 90.00, 4, 2, 6.30),
(10, '2024-04-12', 'NF093', 1, 1, 1, 3, 8, 240.00, 5, 3, 16.80),
(11, '2024-04-12', 'NF094', 1, 2, 2, 1, 9, 270.00, 1, 3, 18.90),
(12, '2024-04-13', 'NF095', 1, 1, 1, 1, 6, 180.00, 2, 1, 12.60),
(13, '2024-04-13', 'NF096', 2, 2, 2, 2, 7, 210.00, 3, 2, 14.70),
(14, '2024-04-13', 'NF097', 2, 1, 1, 1, 8, 240.00, 4, 2, 16.80),
(15, '2024-04-13', 'NF098', 1, 1, 1, 3, 5, 150.00, 5, 3, 10.50),
(16, '2024-04-13', 'NF099', 2, 1, 1, 1, 6, 180.00, 1, 3, 12.60),
(17, '2024-04-14', 'NF100', 1, 1, 1, 1, 7, 210.00, 2, 1, 14.70),
(18, '2024-04-14', 'NF101', 2, 2, 2, 2, 9, 270.00, 3, 2, 18.90),
(19, '2024-04-14', 'NF102', 2, 2, 2, 2, 4, 120.00, 4, 2, 8.40),
(1, '2024-04-14', 'NF103', 2, 1, 1, 3, 8, 240.00, 5, 3, 16.80),
(2, '2024-04-14', 'NF104', 1, 2, 2, 1, 7, 210.00, 1, 3, 14.70),
(3, '2024-04-15', 'NF105', 1, 1, 1, 1, 9, 270.00, 2, 1, 18.90),
(4, '2024-04-15', 'NF106', 2, 2, 2, 2, 6, 180.00, 3, 2, 12.60),
(5, '2024-04-15', 'NF107', 2, 1, 1, 2, 5, 150.00, 4, 2, 10.50),
(6, '2024-04-15', 'NF108', 1, 1, 1, 3, 7, 210.00, 5, 3, 14.70),
(7, '2024-04-15', 'NF109', 1, 1, 1, 1, 4, 120.00, 1, 3, 8.40),
(8, '2024-04-16', 'NF110', 1, 1, 1, 1, 8, 240.00, 2, 1, 16.80),
(9, '2024-04-16', 'NF111', 2, 1, 1, 2, 9, 270.00, 3, 2, 18.90),
(10, '2024-04-16', 'NF112', 2, 2, 2, 1, 6, 180.00, 4, 2, 12.60),
(11, '2024-04-16', 'NF113', 2, 2, 2, 3, 5, 150.00, 5, 3, 10.50),
(12, '2024-04-16', 'NF114', 2, 2, 2, 1, 7, 210.00, 1, 3, 14.70),
(13, '2024-04-17', 'NF115', 1, 1, 1, 1, 9, 270.00, 2, 1, 18.90),
(14, '2024-04-17', 'NF116', 2, 2, 2, 2, 6, 180.00, 3, 2, 12.60),
(15, '2024-04-17', 'NF117', 2, 1, 1, 3, 5, 150.00, 4, 2, 10.50),
(16, '2024-04-17', 'NF118', 2, 2, 2, 1, 8, 240.00, 5, 3, 16.80),
(17, '2024-04-17', 'NF119', 2, 2, 2, 2, 7, 210.00, 1, 3, 14.70),
(18, '2024-04-18', 'NF120', 1, 1, 1, 1, 9, 270.00, 2, 1, 18.90),
(19, '2024-04-18', 'NF121', 2, 2, 2, 2, 6, 180.00, 3, 2, 12.60),
(1, '2024-04-18', 'NF122', 2, 1, 1, 1, 5, 150.00, 4, 2, 10.50),
(2, '2024-04-18', 'NF123', 2, 2, 2, 3, 7, 210.00, 5, 3, 14.70),
(3, '2024-04-18', 'NF124', 1, 1, 1, 2, 4, 120.00, 1, 3, 8.40),
(4, '2024-04-19', 'NF125', 1, 2, 2, 3, 8, 240.00, 2, 1, 16.80);
