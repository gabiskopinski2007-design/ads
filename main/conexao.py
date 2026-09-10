import sqlite3
import os

def conectar_banco():
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, "oficina.db")

    try:
        conexao = sqlite3.connect(caminho)

        return conexao

    except sqlite3.Error as erro:
        print("ERRO AO CONECTAR:")
        print(erro)

        return None