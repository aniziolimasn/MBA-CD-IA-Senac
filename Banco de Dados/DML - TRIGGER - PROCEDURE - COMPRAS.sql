/*
================================================================================
Arquivo: DML - TRIGGER - PROCEDURE - COMPRAS.sql
Finalidade: Automatizar o controle de movimentação de estoque ao registrar compras
Autor: Anizio Neto
Data: 18/07/2024

Descrição Geral:
Este script SQL implementa uma procedure e uma trigger para garantir que, ao inserir
uma nova compra na tabela 'compra', a movimentação de estoque seja registrada ou
atualizada automaticamente na tabela 'mov_estoque'.

Componentes:
- Procedure 'registrar_movimentacao_compra':
  Recebe o id da compra, busca os dados da compra, verifica se já existe movimentação
  para o produto e data, atualiza ou insere a movimentação de estoque conforme o caso.
- Trigger 'after_compra_insert':
  Disparada após o insert na tabela 'compra', chama a procedure para registrar a
  movimentação de estoque correspondente.
================================================================================
*/

USE mydb;
DELIMITER //

-- Procedure responsável por registrar ou atualizar a movimentação de estoque após uma compra
CREATE PROCEDURE registrar_movimentacao_compra (
    IN p_id_compra INT
)
BEGIN
    -- Declaração de variáveis locais
    DECLARE v_id_produto INT;
    DECLARE v_qtd_compra INT;
    DECLARE v_data_compra DATE;
    DECLARE v_saldo_anterior INT;
    DECLARE v_saldo_dia INT;
    DECLARE v_estoque INT;
    DECLARE v_id_mov_estoque INT;

    -- Obter os dados da compra (produto, quantidade e data)
    SELECT produtos_id_produto, qtd_compra, data_compra
    INTO v_id_produto, v_qtd_compra, v_data_compra
    FROM compra
    WHERE id_compra = p_id_compra;

    -- Verificar se já existe uma movimentação para o produto e data
    SELECT id_mov_estoque, saldo_anterior, estoque
    INTO v_id_mov_estoque, v_saldo_anterior, v_estoque
    FROM mov_estoque
    WHERE produtos_id_produto = v_id_produto
      AND data_movimentacao = v_data_compra
    LIMIT 1;

    IF v_id_mov_estoque IS NOT NULL THEN
        -- Se já existe movimentação, atualiza os valores somando a nova compra
        UPDATE mov_estoque
        SET qtd_compra = qtd_compra + v_qtd_compra,
            saldo_dia = saldo_anterior + qtd_compra - qtd_venda,
            estoque = estoque + v_qtd_compra
        WHERE id_mov_estoque = v_id_mov_estoque;
    ELSE
        -- Se não existe movimentação, busca o saldo anterior e estoque do último registro
        SELECT IFNULL(saldo_dia, 0), IFNULL(estoque, 0)
        INTO v_saldo_anterior, v_estoque
        FROM mov_estoque
        WHERE produtos_id_produto = v_id_produto
        ORDER BY data_movimentacao DESC
        LIMIT 1;

        -- Calcula o saldo do dia e o novo estoque
        SET v_saldo_dia = v_saldo_anterior + v_qtd_compra;
        SET v_estoque = v_estoque + v_qtd_compra;

        -- Insere nova movimentação de estoque
        INSERT INTO mov_estoque (
            data_movimentacao, 
            produtos_id_produto, 
            qtd_compra, 
            qtd_venda, 
            saldo_dia, 
            saldo_anterior, 
            estoque
        ) VALUES (
            v_data_compra, 
            v_id_produto, 
            v_qtd_compra, 
            0, -- Sem vendas nesta movimentação
            v_saldo_dia, 
            v_saldo_anterior, 
            v_estoque
        );
    END IF;
END //

DELIMITER ;

---------------------------

DELIMITER //

-- Trigger que executa a procedure após inserir uma nova compra
CREATE TRIGGER after_compra_insert
AFTER INSERT ON compra
FOR EACH ROW
BEGIN
    -- Chama o procedimento registrar_movimentacao_compra passando o id_compra
    CALL registrar_movimentacao_compra(NEW.id_compra);
END //

DELIMITER ;
