# Conecta com o banco de dados
from conexao import conectar_banco
from sqlite3 import Error

# CADASTRAR PEÇA
# Função que cadastra peça
def cadastrar_peca(
    nome,
    quantidade,
    valor,
    fornecedor
):

    # Abre a conexão com o banco de dados.
    conexao = conectar_banco()

    # Verifica se a conexão foi realizada.
    if conexao is None:
        print("ERRO: conexão não foi criada.")
        return

    try:
        # Cria um cursor para executar comandos SQL.
        cursor = conexao.cursor()

        # Comando SQL para cadastrar uma nova peça.
        cursor.execute ( 
            """
            INSERT INTO pecas
            (nome, quantidade, valor, fornecedor)
            VALUES (?, ?, ?, ?)
            """,
            (nome, quantidade, valor, fornecedor)
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
