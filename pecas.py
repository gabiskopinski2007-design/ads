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

# LISTAR TODAS AS PEÇAS
def listar_pecas():

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                SELECT
                    id,
                    nome,
                    quantidade,
                    valor,
                    fornecedor
                FROM pecas
            """

            cursor.execute(sql)

            pecas = cursor.fetchall()

            return pecas

        except Error as erro:
            print(f"Erro ao listar peças: {erro}")
            return []

        finally:
            cursor.close()
            conexao.close()

    return []

# BUSCAR PEÇA PELO ID
def buscar_peca(id):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                SELECT
                    id,
                    nome,
                    quantidade,
                    valor,
                    fornecedor
                FROM pecas
                WHERE id = ?
            """

            cursor.execute(sql, (id))

            peca = cursor.fetchone()

            return peca

        except Error as erro:
            print(f"Erro ao buscar peça: {erro}")
            return None

        finally:
            cursor.close()
            conexao.close()

    return None

# ATUALIZAR PEÇA
def atualizar_peca(
    id,
    nome,
    quantidade,
    valor,
    fornecedor
):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                UPDATE pecas
                SET
                    nome = ?,
                    quantidade = ?,
                    valor = ?,
                    fornecedor = ?
                WHERE id = ?
            """

            valores = (
                nome,
                quantidade,
                valor,
                fornecedor,
                id               
            )

            cursor.execute(sql, valores)

            conexao.commit()

            if cursor.rowcount > 0:
                print("Peça atualizada com sucesso!")
            else:
                print("Peça não encontrada.")

        except Error as erro:
            print(f"Erro ao atualizar peça: {erro}")

        finally:
            cursor.close()
            conexao.close()

# EXCLUIR PEÇA
def excluir_peca(id):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                DELETE FROM pecas
                WHERE id = ?
            """

            cursor.execute(sql, (id))

            conexao.commit()

            if cursor.rowcount > 0:
                print("Peça excluída com sucesso!")
            else:
                print("Peça não encontrada.")

        except Error as erro:
            print(f"Erro ao excluir peça: {erro}")

        finally:
            cursor.close()
            conexao.close()