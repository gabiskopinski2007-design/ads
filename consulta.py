import sqlite3

conexao = sqlite3.connect("oficina.db")
cursor = conexao.cursor()

cursor.execute("""
SELECT clientes.nome, veiculos.placa, veiculos.modelo, servicos.descricao
FROM clientes
JOIN veiculos
ON clientes.id = veiculos.cliente_id
JOIN servicos
ON veiculos.id = servicos.veiculo_id
""")

print(cursor.fetchall())
cursor.execute("SELECT * FROM servicos")
print(cursor.fetchall())
cursor.execute("""
SELECT clientes.nome, veiculos.placa, orcamentos.data, orcamentos.valor_total
FROM clientes
JOIN veiculos
ON clientes.id = veiculos.cliente_id
JOIN orcamentos
ON veiculos.id = orcamentos.veiculo_id
""")

print(cursor.fetchall())