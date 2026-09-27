# Conecta com o banco de dados
from conexao import conectar_banco
from sqlite3 import Error

import conexao

# CADASTRAR ORÇAMENTO
# Função que cadastra orçamento
def cadastrar_orcamento(
    data,
    valor_total,
    veiculo_id
):

    # Abre a conexão com o banco.
    conexao = conectar_banco()

    # Verifica se a conexão foi realizada.
    if conexao is None:
        print("ERRO: conexão não foi criada.")
        return

    try:
        # Cria o cursor para executar comandos SQL.
        cursor = conexao.cursor()
        # Comando SQL para inserir um orçamento.
        cursor.execute (
            """
            INSERT INTO orcamentos
            (data, valor_total, veiculo_id)
            VALUES (?, ?, ?)
            """,
            (data, valor_total, veiculo_id)
        )

        # Confirma a alteração no banco.
        conexao.commit()

    except Error as erro:
        print("ERRO DO SQLITE:")
        print(type(erro).__name__)
        print(erro)

        # Cancela qualquer alteração pendente
        conexao.rollback()

    except Exception as erro:
        print("ERRO:")
        print(type(erro).__name__)
        print(erro)

    finally:
        conexao.close()

# LISTAR TODOS OS ORÇAMENTOS
def listar_orcamentos():

    # Abre a conexão com o banco.
    conexao = conectar_banco()

    # Verifica se a conexão foi realizada.
    if conexao is None:
        print("ERRO: conexão não foi criada.")
        return

    try:
        linhas = conexao.execute(
                    """
                    SELECT o.id, o.data, o.valor_total, v.id, v.placa, c.nome
                    FROM orcamentos o
                    JOIN veiculos v ON v.id = o.veiculo_id
                    JOIN clientes c ON c.id = v.cliente_id
                    ORDER BY o.id
                    """).fetchall()
        return linhas

    except Error as erro:
        print("ERRO DO SQLITE:")
        print(type(erro).__name__)
        print(erro)

        # Cancela qualquer alteração pendente
        conexao.rollback()

    except Exception as erro:
        print("ERRO:")
        print(type(erro).__name__)
        print(erro)

    finally:
        conexao.close()
