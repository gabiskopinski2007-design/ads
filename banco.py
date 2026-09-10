import sqlite3
import os

conexao = sqlite3.connect("oficina.db")

print(os.path.abspath("oficina.db"))

cursor = conexao.cursor()
cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    endereco TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    modelo TEXT,
    ano INTEGER,
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL,
    quilometros INTEGER NOT NULL,
    veiculo_id INTEGER,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    valor REAL NOT NULL,
    fornecedor TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS orcamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    valor_total REAL NOT NULL,
    veiculo_id INTEGER,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
)
""")
conexao.commit()
conexao.close()
print("Banco criado com sucesso!")