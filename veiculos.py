# Conecta no bando de dados
from conexao import conectar_banco
from sqlite3 import Error

# CADASTRAR VEÍCULO
def cadastrar_veiculo(placa, modelo, ano, cliente_id):
    # Abre conexão com o banco
    conexao = conectar_banco()

    if conexao:
        try:

            # Cria o cursor para executar comandos SQL
            cursor = conexao.cursor()

            # Comando SQL para inserir um veículo
            sql = """
                INSERT INTO veiculos
                (placa, modelo, ano, cliente_id)
                VALUES (?, ?, ?, ?)
            """

            # Valores que serão enviados para os ?
            valores = (placa, modelo, ano, cliente_id)

            # Executa o INSERT
            cursor.execute(sql, valores)

            # Confirma a alteração no banco
            conexao.commit()

            print("Veículo cadastrado com sucesso!")

        except Exception as erro:
            print(f"Erro ao cadastrar veículo: {erro}")

        finally:
            # Fecha o cursor
            cursor.close()

            # Fecha a conexão
            conexao.close()

# LISTAR TODOS OS VEÍCULOS
def listar_veiculos():

    # Conecta no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                SELECT
                    id,
                    placa,
                    modelo,
                    ano,
                    cliente_id
                FROM veiculos
            """

            cursor.execute(sql)

            veiculos = cursor.fetchall()

            return veiculos

        except Error as erro:
            print(f"Erro ao listar veículos: {erro}")
            return []

        finally:
            cursor.close()
            conexao.close()

    return []

# BUSCAR VEÍCULO PELO ID
def buscar_veiculo(id):

    # Conectar no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                SELECT
                    id,
                    placa,
                    modelo,
                    ano,
                    cliente_id
                FROM veiculos
                WHERE id = ?
            """

            cursor.execute(sql, (id,))

            veiculo = cursor.fetchone()

            return veiculo

        except Error as erro:
            print(f"Erro ao buscar veículo: {erro}")
            return None

        finally:
            cursor.close()
            conexao.close()

    return None

# ATUALIZAR VEÍCULO
def atualizar_veiculo(id, placa, modelo, ano, cliente_id):

    # Conectar no banco de dados
    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                UPDATE veiculos
                SET
                    placa = ?,
                    modelo = ?,
                    ano = ?,
                    cliente_id = ?
                WHERE id = ?
            """

            valores = (
                placa,
                modelo,
                ano,
                cliente_id,
                id
            )

            cursor.execute(sql, valores)

            conexao.commit()

            if cursor.rowcount > 0:
                print("Veículo atualizado com sucesso!")
            else:
                print("Veículo não encontrado.")

        except Error as erro:
            print(f"Erro ao atualizar veículo: {erro}")

        finally:
            cursor.close()
            conexao.close()

# EXCLUIR VEÍCULO
def excluir_veiculo(id):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                DELETE FROM veiculo
                WHERE id = ?
            """

            cursor.execute(sql, id)

            conexao.commit()

            if cursor.rowcount > 0:
                print("Veículo excluído com sucesso!")
            else:
                print("Veículo não encontrado.")

        except Error as erro:
            print(f"Erro ao excluir veículo: {erro}")

        finally:
            cursor.close()
            conexao.close()

