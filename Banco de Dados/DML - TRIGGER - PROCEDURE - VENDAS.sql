-- -------------------------------------------------------------
-- Script: DML - TRIGGER - PROCEDURE - VENDAS.sql
-- Finalidade: Gerenciar automaticamente a movimentação de estoque
--             ao registrar uma venda, garantindo que o estoque
--             seja atualizado corretamente a cada nova venda.
-- Ambiente: MySQL
-- Autor: Anizio Neto
-- Data: 18/07/2024
-- -------------------------------------------------------------

use mydb;

DELIMITER //

-- =============================================================
-- PROCEDURE: registrar_movimentacao_venda
-- Objetivo: Ao receber o id de uma venda, atualiza ou insere a
--           movimentação de estoque correspondente ao produto
--           vendido, controlando saldo, estoque e histórico.
-- Parâmetro:
--   p_id_venda (INT): identificador da venda registrada
-- =============================================================
CREATE PROCEDURE registrar_movimentacao_venda (
    IN p_id_venda INT
)
BEGIN
    -- Declaração de variáveis locais para manipulação dos dados
    DECLARE v_id_produto INT;         -- ID do produto vendido
    DECLARE v_qtd_venda INT;          -- Quantidade vendida
    DECLARE v_data_venda DATE;        -- Data da venda
    DECLARE v_saldo_anterior INT;     -- Saldo anterior do estoque
    DECLARE v_saldo_dia INT;          -- Saldo do dia após movimentação
    DECLARE v_estoque INT;            -- Estoque atual
    DECLARE v_id_mov_estoque INT;     -- ID da movimentação de estoque

    -- Busca os dados da venda (produto, quantidade, data)
    SELECT produtos_id_produto, qtd_venda, data_emissao_nf
    INTO v_id_produto, v_qtd_venda, v_data_venda
    FROM venda
    WHERE id_venda = p_id_venda;

    -- Verifica se já existe movimentação para o produto na data da venda
    SELECT id_mov_estoque, saldo_anterior, estoque
    INTO v_id_mov_estoque, v_saldo_anterior, v_estoque
    FROM mov_estoque
    WHERE produtos_id_produto = v_id_produto
      AND data_movimentacao = v_data_venda
    LIMIT 1;

    IF v_id_mov_estoque IS NOT NULL THEN
        -- Caso já exista movimentação, atualiza os valores de venda e estoque
        UPDATE mov_estoque
        SET qtd_venda = qtd_venda + v_qtd_venda,
            saldo_dia = saldo_anterior + qtd_compra - qtd_venda,
            estoque = estoque - v_qtd_venda
        WHERE id_mov_estoque = v_id_mov_estoque;
    ELSE
        -- Caso não exista movimentação, busca o saldo anterior mais recente
        SELECT IFNULL(saldo_dia, 0), IFNULL(estoque, 0)
        INTO v_saldo_anterior, v_estoque
        FROM mov_estoque
        WHERE produtos_id_produto = v_id_produto
        ORDER BY data_movimentacao DESC
        LIMIT 1;

        -- Calcula o saldo do dia e estoque após a venda
        SET v_saldo_dia = v_saldo_anterior - v_qtd_venda;
        SET v_estoque = v_estoque - v_qtd_venda;

        -- Insere nova movimentação de estoque para o produto na data
        INSERT INTO mov_estoque (
            data_movimentacao, 
            produtos_id_produto, 
            qtd_compra, 
            qtd_venda, 
            saldo_dia, 
            saldo_anterior, 
            estoque
        ) VALUES (
            v_data_venda, 
            v_id_produto, 
            0, -- Sem compras nesta movimentação
            v_qtd_venda, 
            v_saldo_dia, 
            v_saldo_anterior, 
            v_estoque
        );
    END IF;
END //

-- =============================================================
-- TRIGGER: after_venda_insert
-- Objetivo: Após inserir uma nova venda, chama automaticamente
--           o procedimento para registrar a movimentação de estoque
-- =============================================================
CREATE TRIGGER after_venda_insert
AFTER INSERT ON venda
FOR EACH ROW
BEGIN
    -- Chama o procedimento registrar_movimentacao_venda passando o id_venda
    CALL registrar_movimentacao_venda(NEW.id_venda);
END //

DELIMITER ;

-- =============================================================
-- RESUMO DA FINALIDADE DO SCRIPT
-- -------------------------------------------------------------
-- Este script automatiza o controle de estoque ao registrar vendas:
-- 1. Ao inserir uma venda, a trigger chama o procedimento.
-- 2. O procedimento verifica se já existe movimentação de estoque
--    para o produto e data. Se sim, atualiza; se não, insere nova.
-- 3. Garante que o estoque e o saldo diário estejam sempre corretos.
-- 4. Evita inconsistências e facilita auditoria do estoque.
-- -------------------------------------------------------------
