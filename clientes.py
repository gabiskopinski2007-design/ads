from conexao import conectar_banco
from sqlite3 import Error

# CADASTRAR CLIENTE
def cadastrar_cliente(nome, telefone, endereco):
    # Conecta no banco de dados
    conexao = conectar_banco()

    if conexao is None:
        print("ERRO: conexão não foi criada.")
        return

    try:
        cursor = conexao.cursor()

        # Mostra exatamente qual banco está sendo usado
        cursor.execute("PRAGMA database_list")
        banco = cursor.fetchall()

        # Verifica a estrutura da tabela clientes
        cursor.execute("PRAGMA table_info(clientes)")
        campos = cursor.fetchall()

        cursor.execute(
            """
            INSERT INTO clientes (nome, telefone, endereco)
            VALUES (?, ?, ?)
            """,
            (nome, telefone, endereco)
        )

        # Salva no banco
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

# FUNÇÃO PARA LISTAR TODOS OS CLIENTES
def listar_clientes():
    # Conecta no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:

            # Cria um cursor para executar o SQL
            cursor = conexao.cursor()

            # Comando SQL para buscar todos os clientes
            cursor.execute("""
                SELECT id, nome, telefone, endereco
                FROM clientes
            """)

            # Recupera todos os registros encontrados
            clientes = cursor.fetchall()

            # Retorna os clientes para quem chamou a função
            return clientes

        except Error as erro:
            print(f"Erro ao listar clientes: {erro}")
            return []

        finally:
            cursor.close()
            conexao.close()

    return []

# FUNÇÃO PARA BUSCAR UM CLIENTE PELO ID
def buscar_cliente(id):
    # Conecta no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            # Busca somente o cliente que possui o ID informado
            cursor.execute("""
                SELECT id, nome, telefone, endereco
                FROM clientes
                WHERE id = ?
            """, (id,)
            )

            # Pega somente um resultado
            cliente = cursor.fetchone()

            return cliente

        except Error as erro:
            print(f"Erro ao buscar cliente: {erro}")
            return None

        finally:
            cursor.close()
            conexao.close()

    return None

# FUNÇÃO PARA ATUALIZAR UM CLIENTE
def atualizar_cliente(id, nome, telefone, endereco):
    # Conecta no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:

            cursor = conexao.cursor()

            # Comando SQL para alterar os dados do cliente
            cursor.execute(
                """
                UPDATE clientes
                SET nome = ?,
                    telefone = ?,
                    endereco = ?
                WHERE id = ?
            """,(nome, telefone, endereco, id)
            )
            # Confirma a alteração
            conexao.commit()

            # Verifica se algum cliente foi alterado
            if cursor.rowcount > 0:
                print("Cliente atualizado com sucesso!")
            else:
                print("Cliente não encontrado.")

        except Error as erro:
            print(f"Erro ao atualizar cliente: {erro}")

        finally:
            cursor.close()
            conexao.close()

# FUNÇÃO PARA EXCLUIR UM CLIENTE
def excluir_cliente(id):
    # Conecta no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:

            cursor = conexao.cursor()

            # Comando SQL para excluir o cliente pelo ID
            cursor.execute (
                """
                DELETE FROM clientes
                WHERE id = ?
            """, (id,)
            )
            # Confirma a exclusão
            conexao.commit()

            # Verifica se algum registro foi excluído
            if cursor.rowcount > 0:
                print("Cliente excluído com sucesso!")
            else:
                print("Cliente não encontrado.")

        except Error as erro:
            print(f"Erro ao excluir cliente: {erro}")

        finally:
            cursor.close()
            conexao.close()
