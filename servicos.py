# Conecta com o banco de dados
from conexao import conectar_banco
from sqlite3 import Error

# CADASTRAR SERVIÇO
def cadastrar_servico(
    descricao,
    valor,
    data,
    quilometros,
    veiculo_id
):
    # Conecta ao banco de dados.
    conexao = conectar_banco()

    # Verifica se conseguiu estabelecer a conexão.
    if conexao:

        try:
            # Cria o cursor para executar o SQL.
            cursor = conexao.cursor()

            # Comando SQL responsável por inserir um novo serviço na tabela servicos.
            sql = """
                INSERT INTO servicos
                (descricao, valor, data, quilometros, veiculo_id)
                VALUES (?, ?, ?, ?, ?)
            """

            # Valores que serão enviados para o banco.
            valores = (
                descricao,
                valor,
                data,
                quilometros,
                veiculo_id
            )

            # Executa o comando INSERT.
            cursor.execute(sql, valores)

            # Confirma a alteração no banco.
            conexao.commit()

            # Mensagem exibida quando o cadastro funciona.
            print("Serviço cadastrado com sucesso!")

        # Captura possíveis erros.
        except Error as erro:

            # Mostra o erro ocorrido.
            print(f"Erro ao cadastrar serviço: {erro}")

        finally:
            # Fecha o cursor.
            cursor.close()

            # Fecha a conexão com o banco.
            conexao.close()

# LISTAR TODOS OS SERVIÇOS
def listar_servicos():

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                SELECT
                    id,
                    descricao,
                    valor,
                    data,
                    quilometros,
                    veiculo_id
                FROM servicos
            """

            cursor.execute(sql)

            servicos = cursor.fetchall()

            return servicos

        except Error as erro:
            print(f"Erro ao listar serviços: {erro}")
            return []

        finally:
            cursor.close()
            conexao.close()

    return []

# BUSCAR SERVIÇO PELO ID
def buscar_servico(id):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                SELECT
                    id,
                    descricao,
                    valor,
                    data,
                    quilometros,
                    veiculo_id
                FROM servicos
                WHERE id = ?
            """

            cursor.execute(sql, (id,))

            servico = cursor.fetchone()

            return servico

        except Error as erro:
            print(f"Erro ao buscar serviço: {erro}")
            return None

        finally:
            cursor.close()
            conexao.close()

    return None

# ATUALIZAR SERVIÇO
def atualizar_servico(
    id,
    descricao,
    valor,
    data,
    quilometros,
    veiculo_id
):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                UPDATE servicos
                SET
                    descricao = ?,
                    valor = ?,
                    data = ?,
                    quilometros = ?,
                    veiculo_id = ?
                WHERE id = ?
            """

            valores = (
                descricao,
                valor,
                data,
                quilometros,
                veiculo_id,
                id
            )

            cursor.execute(sql, valores)

            conexao.commit()

            if cursor.rowcount > 0:
                print("Serviço atualizado com sucesso!")
            else:
                print("Serviço não encontrado.")

        except Error as erro:
            print(f"Erro ao atualizar serviço: {erro}")

        finally:
            cursor.close()
            conexao.close()

# EXCLUIR SERVIÇO
def excluir_servico(id):

    conexao = conectar_banco()

    if conexao:
        try:
            cursor = conexao.cursor()

            sql = """
                DELETE FROM servicos
                WHERE id = ?
            """

            cursor.execute(sql, (id,))

            conexao.commit()

            if cursor.rowcount > 0:
                print("Serviço excluído com sucesso!")
            else:
                print("Serviço não encontrado.")

        except Error as erro:
            print(f"Erro ao excluir serviço: {erro}")

        finally:
            cursor.close()
            conexao.close()