-- -----------------------------------------------------
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS: mydb
-- -----------------------------------------------------
-- Este script foi gerado pelo MySQL Workbench para criar o banco de dados 'mydb' e suas tabelas principais.
-- Ele define as estruturas, chaves primárias, relacionamentos e restrições necessárias para o funcionamento do sistema.
-- Cada tabela representa uma entidade do negócio, como produtos, categorias, funcionários, clientes, etc.
-- Comentários explicativos foram adicionados para facilitar a compreensão e manutenção do código.

-- Desabilita verificações temporariamente para evitar erros durante a criação das tabelas e relacionamentos
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Criação do schema (banco de dados) 'mydb'
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Tabela 'categorias'
-- Armazena as categorias dos produtos.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`categorias` (
  `id_categoria` INT NOT NULL AUTO_INCREMENT, -- Identificador único da categoria
  `desc_categoria` VARCHAR(45) NOT NULL,      -- Descrição da categoria
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'produtos'
-- Armazena os produtos comercializados, vinculados a uma categoria.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`produtos` (
  `id_produto` INT NOT NULL AUTO_INCREMENT,           -- Identificador único do produto
  `desc_produto` VARCHAR(100) NOT NULL,               -- Descrição do produto
  `status_produto` VARCHAR(45) NOT NULL,              -- Status (ativo, inativo, etc.)
  `data_cadastro` DATE NOT NULL,                      -- Data de cadastro do produto
  `preco_custo` DECIMAL NULL,                         -- Preço de custo
  `preco_venda` DECIMAL NULL,                         -- Preço de venda
  `categorias_id_categoria` INT NOT NULL,             -- Chave estrangeira para categoria
  PRIMARY KEY (`id_produto`),
  INDEX `fk_produtos_categorias_idx` (`categorias_id_categoria` ASC) INVISIBLE,
  CONSTRAINT `fk_produtos_categorias`
    FOREIGN KEY (`categorias_id_categoria`)
    REFERENCES `mydb`.`categorias` (`id_categoria`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'remuneracao'
-- Define os tipos de remuneração e percentuais de comissão dos funcionários.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`remuneracao` (
  `id_remuneracao` INT NOT NULL AUTO_INCREMENT,      -- Identificador único da remuneração
  `tipo_remuneracao` VARCHAR(45) NOT NULL,           -- Tipo (salário, comissão, etc.)
  `percentual_comissao` DECIMAL(4,4) NOT NULL,       -- Percentual de comissão
  PRIMARY KEY (`id_remuneracao`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'funcionarios'
-- Armazena os dados dos funcionários da empresa.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`funcionarios` (
  `id_funcionarios` INT NOT NULL AUTO_INCREMENT,     -- Identificador único do funcionário
  `nome` VARCHAR(45) NOT NULL,                       -- Nome do funcionário
  `cpf` VARCHAR(11) NOT NULL,                        -- CPF do funcionário
  `data_nasc` DATE NOT NULL,                         -- Data de nascimento
  `sexo` TEXT(1) NOT NULL,                           -- Sexo (M/F)
  `data_admissao` DATE NOT NULL,                     -- Data de admissão
  `cargo` VARCHAR(100) NOT NULL,                     -- Cargo do funcionário
  `formacao` VARCHAR(45) NOT NULL,                   -- Formação acadêmica
  `url_imagem` VARCHAR(200) NULL,                    -- URL da imagem do funcionário
  `cidade` VARCHAR(100) NOT NULL,                    -- Cidade de residência
  `uf` TEXT(2) NOT NULL,                             -- Unidade Federativa (UF)
  `endereco` VARCHAR(200) NOT NULL,                  -- Endereço completo
  `remuneracao_id_remuneracao` INT NOT NULL,         -- Chave estrangeira para remuneração
  PRIMARY KEY (`id_funcionarios`),
  INDEX `fk_funcionarios_remuneracao1_idx` (`remuneracao_id_remuneracao` ASC) VISIBLE,
  CONSTRAINT `fk_funcionarios_remuneracao1`
    FOREIGN KEY (`remuneracao_id_remuneracao`)
    REFERENCES `mydb`.`remuneracao` (`id_remuneracao`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'cliente'
-- Armazena os dados dos clientes.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`cliente` (
  `id_cliente` INT NOT NULL AUTO_INCREMENT,          -- Identificador único do cliente
  `nome_cliente` VARCHAR(200) NOT NULL,              -- Nome do cliente
  `tipo_cliente` TEXT(2) NOT NULL,                   -- Tipo de cliente (PF/PJ)
  `cpf_cnpj` VARCHAR(14) NOT NULL,                   -- CPF ou CNPJ do cliente
  `uf` TEXT(2) NOT NULL,                             -- Unidade Federativa (UF)
  `cidade` VARCHAR(100) NOT NULL,                    -- Cidade de residência
  `endereco` VARCHAR(200) NOT NULL,                  -- Endereço completo
  `teleforne` VARCHAR(45) NULL,                      -- Telefone de contato
  `e-mail` VARCHAR(100) NULL,                        -- E-mail de contato
  `data_cadastro` DATE NOT NULL,                     -- Data de cadastro do cliente
  `status_cliente` VARCHAR(45) NOT NULL,             -- Status do cliente (ativo, inativo, etc.)
  PRIMARY KEY (`id_cliente`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'impostos'
-- Armazena os tipos de impostos e suas alíquotas.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`impostos` (
  `id_impostos` INT NOT NULL AUTO_INCREMENT,         -- Identificador único do imposto
  `nome_imposto` VARCHAR(100) NOT NULL,              -- Nome do imposto
  `perc_aliquota` DECIMAL(5,2) NOT NULL,             -- Percentual da alíquota
  PRIMARY KEY (`id_impostos`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'fornecedor'
-- Armazena os dados dos fornecedores.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`fornecedor` (
  `id_fornecedor` INT NOT NULL AUTO_INCREMENT,       -- Identificador único do fornecedor
  `nome_fornecedor` VARCHAR(100) NOT NULL,           -- Nome do fornecedor
  `tipo_fornecedor` TEXT(2) NOT NULL,                -- Tipo de fornecedor (PF/PJ)
  `cpf_cnpj` VARCHAR(14) NOT NULL,                   -- CPF ou CNPJ do fornecedor
  `uf` TEXT(2) NOT NULL,                             -- Unidade Federativa (UF)
  `cidade` VARCHAR(100) NOT NULL,                    -- Cidade de residência
  `endereco` VARCHAR(200) NOT NULL,                  -- Endereço completo
  `teleforne` VARCHAR(45) NULL,                      -- Telefone de contato
  `e-mail` VARCHAR(100) NULL,                        -- E-mail de contato
  `data_cadastro` DATE NOT NULL,                     -- Data de cadastro do fornecedor
  `status_fornecedor` VARCHAR(45) NOT NULL,          -- Status do fornecedor (ativo, inativo, etc.)
  PRIMARY KEY (`id_fornecedor`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'promo_desc'
-- Armazena as promoções e descontos aplicáveis aos produtos.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`promo_desc` (
  `id_promo_desc` INT NOT NULL AUTO_INCREMENT,       -- Identificador único da promoção/desconto
  `nome_promocao` VARCHAR(100) NOT NULL,             -- Nome da promoção
  `perc_desconto` DECIMAL(5,2) NOT NULL,             -- Percentual de desconto
  `data_inicio` DATE NOT NULL,                       -- Data de início da promoção
  `data_fim` DATE NOT NULL,                          -- Data de término da promoção
  PRIMARY KEY (`id_promo_desc`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'canal'
-- Armazena os canais de venda.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`canal` (
  `id_canal` INT NOT NULL AUTO_INCREMENT,            -- Identificador único do canal
  `nome_canal` VARCHAR(50) NOT NULL,                 -- Nome do canal
  PRIMARY KEY (`id_canal`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'meios_pgto'
-- Armazena os meios de pagamento aceitos.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`meios_pgto` (
  `id_meio_pgto` INT NOT NULL AUTO_INCREMENT,        -- Identificador único do meio de pagamento
  `nome_meio_pgto` VARCHAR(45) NOT NULL,             -- Nome do meio de pagamento
  `perc_taxa_adm` DECIMAL(4,3) NOT NULL,             -- Percentual da taxa administrativa
  PRIMARY KEY (`id_meio_pgto`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'mov_estoque'
-- Armazena as movimentações de estoque dos produtos.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`mov_estoque` (
  `id_mov_estoque` INT NOT NULL AUTO_INCREMENT,      -- Identificador único da movimentação
  `data_movimentacao` DATE NOT NULL,                 -- Data da movimentação
  `produtos_id_produto` INT NOT NULL,                -- Chave estrangeira para produto
  `qtd_compra` INT NOT NULL,                         -- Quantidade comprada
  `qtd_venda` INT NOT NULL,                          -- Quantidade vendida
  `saldo_dia` INT NOT NULL,                          -- Saldo do dia
  `saldo_anterior` INT NOT NULL,                     -- Saldo anterior
  `estoque` INT NOT NULL,                            -- Estoque atual
  PRIMARY KEY (`id_mov_estoque`),
  INDEX `fk_mov_estoque_produtos1_idx` (`produtos_id_produto` ASC) VISIBLE,
  CONSTRAINT `fk_mov_estoque_produtos1`
    FOREIGN KEY (`produtos_id_produto`)
    REFERENCES `mydb`.`produtos` (`id_produto`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'compra'
-- Armazena os dados das compras realizadas.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`compra` (
  `id_compra` INT NOT NULL AUTO_INCREMENT,           -- Identificador único da compra
  `nf_fornecedor` VARCHAR(45) NOT NULL,              -- Nota fiscal do fornecedor
  `fornecedor_id_fornecedor` INT NOT NULL,           -- Chave estrangeira para fornecedor
  `data_compra` DATE NOT NULL,                       -- Data da compra
  `data_emissao_nf` DATE NOT NULL,                   -- Data de emissão da nota fiscal
  `funcionarios_id_funcionarios` INT NOT NULL,       -- Chave estrangeira para funcionário
  `qtd_compra` INT NOT NULL,                         -- Quantidade comprada
  `preco_compra` INT NOT NULL,                       -- Preço de compra
  `produtos_id_produto` INT NOT NULL,                -- Chave estrangeira para produto
  `impostos_id_impostos` INT NOT NULL,               -- Chave estrangeira para imposto
  PRIMARY KEY (`id_compra`),
  INDEX `fk_compra_fornecedor1_idx` (`fornecedor_id_fornecedor` ASC) VISIBLE,
  INDEX `fk_compra_funcionarios1_idx` (`funcionarios_id_funcionarios` ASC) VISIBLE,
  INDEX `fk_compra_produtos1_idx` (`produtos_id_produto` ASC) VISIBLE,
  INDEX `fk_compra_impostos1_idx` (`impostos_id_impostos` ASC) VISIBLE,
  CONSTRAINT `fk_compra_fornecedor1`
    FOREIGN KEY (`fornecedor_id_fornecedor`)
    REFERENCES `mydb`.`fornecedor` (`id_fornecedor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_compra_funcionarios1`
    FOREIGN KEY (`funcionarios_id_funcionarios`)
    REFERENCES `mydb`.`funcionarios` (`id_funcionarios`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_compra_produtos1`
    FOREIGN KEY (`produtos_id_produto`)
    REFERENCES `mydb`.`produtos` (`id_produto`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_compra_impostos1`
    FOREIGN KEY (`impostos_id_impostos`)
    REFERENCES `mydb`.`impostos` (`id_impostos`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabela 'venda'
-- Armazena os dados das vendas realizadas.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`venda` (
  `id_venda` INT NOT NULL AUTO_INCREMENT,            -- Identificador único da venda
  `cliente_id_cliente` INT NOT NULL,                 -- Chave estrangeira para cliente
  `data_emissao_nf` DATE NOT NULL,                   -- Data de emissão da nota fiscal
  `nf_venda` VARCHAR(45) NOT NULL,                   -- Nota fiscal da venda
  `promo_desc_id_promo_desc` INT NOT NULL,           -- Chave estrangeira para promoção/desconto
  `meios_pgto_id_meio_pgto` INT NOT NULL,            -- Chave estrangeira para meio de pagamento
  `canal_id_canal` INT NOT NULL,                     -- Chave estrangeira para canal de venda
  `funcionarios_id_funcionarios` INT NOT NULL,       -- Chave estrangeira para funcionário
  `qtd_venda` INT NOT NULL,                          -- Quantidade vendida
  `preco_venda` VARCHAR(45) NOT NULL,                -- Preço de venda
  `produtos_id_produto` INT NOT NULL,                -- Chave estrangeira para produto
  `impostos_id_impostos` INT NOT NULL,               -- Chave estrangeira para imposto
  `valor_imposto` INT NOT NULL,                      -- Valor do imposto
  PRIMARY KEY (`id_venda`),
  INDEX `fk_venda_cliente1_idx` (`cliente_id_cliente` ASC) VISIBLE,
  INDEX `fk_venda_promo_desc1_idx` (`promo_desc_id_promo_desc` ASC) VISIBLE,
  INDEX `fk_venda_meios_pgto1_idx` (`meios_pgto_id_meio_pgto` ASC) VISIBLE,
  INDEX `fk_venda_canal1_idx` (`canal_id_canal` ASC) VISIBLE,
  INDEX `fk_venda_funcionarios1_idx` (`funcionarios_id_funcionarios` ASC) VISIBLE,
  INDEX `fk_venda_produtos1_idx` (`produtos_id_produto` ASC) VISIBLE,
  INDEX `fk_venda_impostos1_idx` (`impostos_id_impostos` ASC) VISIBLE,
  CONSTRAINT `fk_venda_cliente1`
    FOREIGN KEY (`cliente_id_cliente`)
    REFERENCES `mydb`.`cliente` (`id_cliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_venda_promo_desc1`
    FOREIGN KEY (`promo_desc_id_promo_desc`)
    REFERENCES `mydb`.`promo_desc` (`id_promo_desc`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_venda_meios_pgto1`
    FOREIGN KEY (`meios_pgto_id_meio_pgto`)
    REFERENCES `mydb`.`meios_pgto` (`id_meio_pgto`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_venda_canal1`
    FOREIGN KEY (`canal_id_canal`)
    REFERENCES `mydb`.`canal` (`id_canal`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_venda_funcionarios1`
    FOREIGN KEY (`funcionarios_id_funcionarios`)
    REFERENCES `mydb`.`funcionarios` (`id_funcionarios`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_venda_produtos1`
    FOREIGN KEY (`produtos_id_produto`)
    REFERENCES `mydb`.`produtos` (`id_produto`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_venda_impostos1`
    FOREIGN KEY (`impostos_id_impostos`)
    REFERENCES `mydb`.`impostos` (`id_impostos`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
